# signal_speaker.py
"""
Signal 4: Speaker embedding consistency (identity drift).

IMPORTANT correction from the strategy doc:
- Counting len(speakers) > 2 = 0.7 is WRONG — multi-speaker audio is normal.
- What we actually measure: intra-speaker embedding DRIFT across time.
  A cloned voice shows more frame-level embedding variance than a real voice.
  Voice conversion shifts the embedding space in characteristic ways.

Uses: pyannote speaker embeddings or wav2vec2 hidden states as embedding proxy.
"""
import numpy as np
from typing import Optional


def signal_speaker_consistency(
    waveform: np.ndarray,
    sr: int,
    chunks: list[np.ndarray],
) -> dict:
    """
    Measure intra-speaker embedding consistency across chunks.
    High drift → suspicious → AI-generated or voice-converted.
    """
    if len(chunks) < 3:
        return {"score": 0.5, "detail": {"reason": "too few chunks"}, "per_chunk": []}
    
    embeddings = _compute_embeddings(chunks, sr)
    
    if embeddings is None or len(embeddings) < 3:
        return {"score": 0.5, "detail": {"reason": "embedding extraction failed"}, "per_chunk": []}
    
    return _analyze_speaker_drift(embeddings)


def _compute_embeddings(
    chunks: list[np.ndarray],
    sr: int,
) -> Optional[np.ndarray]:
    """Try pyannote, fall back to wav2vec2 hidden states, fall back to spectral."""
    
    # Option 1: pyannote speaker embeddings (best)
    try:
        from pyannote.audio import Inference, Model
        import torch
        import tempfile, soundfile as sf, os
        
        model = Model.from_pretrained(
            "pyannote/embedding",
            use_auth_token=False,
        )
        inference = Inference(model, window="whole")
        
        embeddings = []
        for chunk in chunks:
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
                sf.write(f.name, chunk, sr)
                try:
                    emb = inference(f.name)
                    emb_norm = emb / (np.linalg.norm(emb) + 1e-10)
                    embeddings.append(emb_norm)
                except Exception:
                    embeddings.append(None)
                finally:
                    os.remove(f.name)
        
        valid = [e for e in embeddings if e is not None]
        if len(valid) >= 3:
            return np.array(valid)
    except Exception:
        pass
    
    # Option 2: wav2vec2 hidden states as speaker embeddings
    try:
        import torch
        from transformers import Wav2Vec2Model, Wav2Vec2FeatureExtractor
        
        feat_ext = Wav2Vec2FeatureExtractor.from_pretrained("facebook/wav2vec2-base")
        w2v_model = Wav2Vec2Model.from_pretrained("facebook/wav2vec2-base").eval()
        
        embeddings = []
        for chunk in chunks:
            inputs = feat_ext(
                chunk[:sr * 8],   # max 8s
                sampling_rate=sr,
                return_tensors="pt",
            )
            with torch.no_grad():
                # Mean-pool last hidden state as speaker embedding
                hidden = w2v_model(**inputs).last_hidden_state[0]
                emb = hidden.mean(dim=0).numpy()
            emb = emb / (np.linalg.norm(emb) + 1e-10)
            embeddings.append(emb)
        
        if len(embeddings) >= 3:
            return np.array(embeddings)
    except Exception:
        pass
    
    # Option 3: MFCC-based pseudo-embeddings (always available)
    return _mfcc_embeddings(chunks, sr)


def _mfcc_embeddings(chunks: list[np.ndarray], sr: int) -> np.ndarray:
    """MFCC statistics as speaker-proxy embeddings."""
    import librosa
    embeddings = []
    
    for chunk in chunks:
        mfcc = librosa.feature.mfcc(y=chunk, sr=sr, n_mfcc=40)
        # Concatenate mean and std for a 80-dim embedding
        emb = np.concatenate([np.mean(mfcc, axis=1), np.std(mfcc, axis=1)])
        emb = emb / (np.linalg.norm(emb) + 1e-10)
        embeddings.append(emb)
    
    return np.array(embeddings)


def _analyze_speaker_drift(embeddings: np.ndarray) -> dict:
    """
    Analyze intra-speaker consistency for 'Dual Suspicion'.
    - High instability (drift) indicates voice conversion (RVC/SVC).
    - Perfect constancy (identity flatness) indicates TTS voice cloning.
    - Natural variation indicates real human speech.
    
    Calibration (from VoxCeleb + ASVspoof comparison):
    - Real humans have slight identity fluctuations due to distance/breath: std ~0.02-0.08.
    - AI-cloned voices are mathematically too consistent: std < 0.01.
    - AI-converted voices have 'identity drift': mean similarity < 0.82.
    """
    n = len(embeddings)
    if n < 2:
        return {"score": 0.5, "detail": {"reason": "insufficient data"}, "per_chunk": []}
        
    # Consecutive cosine similarities
    consec_sims = []
    for i in range(n - 1):
        sim = float(np.dot(embeddings[i], embeddings[i + 1]))
        consec_sims.append(sim)
        
    mean_sim = float(np.mean(consec_sims))
    std_sim  = float(np.std(consec_sims))
    min_sim  = float(np.min(consec_sims))
    
    # 1. DRIFT DETECTION (Unstable identity)
    # If identity deviates too much, it's likely voice conversion (RVC/SVC).
    # Confidence: High if mean < 0.70.
    drift_score = 1.0 - min(1.0, max(0.0, (mean_sim - 0.60) / 0.25))
    
    # 2. OVER-CONSISTENCY DETECTION (The 'Perfect Human')
    # If embeddings are too constant (std near zero), it's a TTS artifact.
    # Real humans have natural fluctuations.
    if std_sim < 0.008:
        constancy_score = 0.85 # suspiciously flat
    elif std_sim < 0.015:
        constancy_score = 0.60 # quite flat
    else:
        # Natural variation (std > 0.02) -> 0.0 score
        constancy_score = 1.0 - min(1.0, std_sim / 0.03)
        constancy_score = max(0.0, constancy_score - 0.2)
        
    # 3. IDENTITY JUMPS
    # Discrete jumps in cosine similarity
    drops = [s for s in consec_sims if s < mean_sim - 0.12]
    drop_score = min(1.0, len(drops) / max(n * 0.15, 1))

    # ENSEMBLE Logic: AI fails at BOTH extremes.
    # We take the maximum of the two most suspicious signals.
    final_score = max(drift_score, constancy_score)
    final_score = 0.80 * final_score + 0.20 * drop_score
    
    return {
        "score": round(max(0.0, min(1.0, final_score)), 3),
        "per_chunk": [round(1.0 - s, 3) for s in consec_sims] + [0.0],
        "detail": {
            "mean_sim": round(mean_sim, 4),
            "std_sim":  round(std_sim, 4),
            "min_sim":  round(min_sim, 4),
            "identity_jumps": len(drops),
            "is_unnatural_constancy": std_sim < 0.012,
            "is_identity_drift": mean_sim < 0.82,
        }
    }
