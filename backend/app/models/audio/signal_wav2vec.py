# signal_wav2vec.py (Now acting as AST ASVSpoof 5)
"""
Signal 1: SSL/Spectrogram-based deepfake classifier.

Model: AST-ASVspoof5-Synthetic-Voice-Detection (Audio Spectrogram Transformer)
This is the single strongest SOTA signal for detecting TTS/voice-conversion,
trained on the latest ASVSpoof 2024/2025 dataset.
"""

import torch
import torch.nn.functional as F
import numpy as np
import os
import threading
from transformers import (
    AutoFeatureExtractor,
    AutoModelForAudioClassification,
)
from app.models.loader_sync import MODEL_LOAD_LOCK

_model = None
_processor = None
_ai_label_idx = None
_load_lock = threading.Lock()
TARGET_SR = 16000


def _load_model():
    global _model, _processor, _ai_label_idx
    with _load_lock:
        if _model is not None:
            return

        # Primary SOTA: AST fine-tuned for audio deepfake on ASVSpoof 5
        model_id = "MattyB95/AST-ASVspoof5-Synthetic-Voice-Detection"

        token = os.getenv("HF_TOKEN")
        try:
            print(f"Loading {model_id} (AST ASVSpoof5 - CPU)...")
            # torchaudio DLL bypass is handled globally in app/main.py
            # The AST feature extractor will use its numpy mel-filterbank fallback
            _processor = AutoFeatureExtractor.from_pretrained(model_id, token=token)
            with MODEL_LOAD_LOCK:
                _model = (
                    AutoModelForAudioClassification.from_pretrained(
                        model_id, token=token, low_cpu_mem_usage=False, device_map=None
                    )
                    .to("cpu")
                    .eval()
                )
            _ai_label_idx = _detect_ai_label_index()
            print(f"[OK] AST ASVSpoof5 loaded on CPU. AI label index: {_ai_label_idx}")
            return
                
        except Exception as e:
            print(f"Primary AST model failed ({e}), trying fallback...")

        # Fallback to legacy Wav2Vec2
        model_id = "abhishtagatya/wav2vec2-base-960h-asv19-deepfake"
        try:
            _processor = AutoFeatureExtractor.from_pretrained(model_id, token=token)
            with MODEL_LOAD_LOCK:
                _model = (
                    AutoModelForAudioClassification.from_pretrained(
                        model_id, token=token, low_cpu_mem_usage=False, device_map=None
                    )
                    .to("cpu")
                    .eval()
                )
            _ai_label_idx = _detect_ai_label_index()
            print(
                f"[OK] Fallback Wav2Vec2 loaded on CPU. AI label index: {_ai_label_idx}"
            )
        except Exception as e2:
            print(f"Both models failed: {e2}. Wav2Vec signal will return 0.5.")
            _model = None


def _detect_ai_label_index() -> int:
    """Empirically detect which output index = 'fake/AI' label."""
    if hasattr(_model.config, "id2label"):
        labels = _model.config.id2label
        print(f"  Model labels: {labels}")
        for idx, label in labels.items():
            if any(
                k in label.lower() for k in ["fake", "spoof", "synthetic", "bonafide"]
            ):
                # "bonafide" = real → NOT the AI label
                if "bonafide" not in label.lower() and "real" not in label.lower():
                    return int(idx)
        # If only "bonafide" label found, AI = the OTHER label
        for idx, label in labels.items():
            if "bonafide" in label.lower() or "real" in label.lower():
                # AI label is the opposite index
                all_indices = list(labels.keys())
                return int([i for i in all_indices if i != idx][0])

    # Fallback: test with silence (should score as suspicious/fake)
    silence = np.zeros(TARGET_SR * 2, dtype=np.float32)
    inputs = _processor(silence, sampling_rate=TARGET_SR, return_tensors="pt")
    with torch.no_grad():
        probs = F.softmax(_model(**inputs).logits, dim=-1)[0]
    # Silence is unnatural → whichever index is higher = likely AI index
    return int(probs.argmax().item())


def _amplify(score: float, power: float = 0.72) -> float:
    s = max(0.0, min(1.0, score))
    if s > 0.5:
        return 0.5 + 0.5 * (((s - 0.5) / 0.5) ** power)
    return 0.5 - 0.5 * (((0.5 - s) / 0.5) ** power)


def signal_wav2vec(chunks: list[np.ndarray]) -> dict:
    """
    Run Wav2Vec2 deepfake classifier on each chunk.
    Returns per-chunk scores and aggregate.
    """
    _load_model()

    if _model is None or not chunks:
        return {
            "score": 0.5,
            "detail": {"reason": "model unavailable"},
            "per_chunk": [],
        }

    chunk_scores = []
    try:
        # Pytorch Tensor Batching (5x-10x speedup)
        batch_in = [chunk[: TARGET_SR * 10] for chunk in chunks]

        inputs = _processor(
            batch_in,
            sampling_rate=TARGET_SR,
            return_tensors="pt",
            padding=True,
        )

        with torch.no_grad():
            inputs = {k: v.to("cpu") for k, v in inputs.items()}
            logits = _model(**inputs).logits
            probs = F.softmax(logits, dim=-1)

        for i in range(len(chunks)):
            raw = float(probs[i][_ai_label_idx].item())
            chunk_scores.append(_amplify(raw))

    except Exception as e:
        print(f"AST/Wav2Vec batch inference failed: {e}")
        chunk_scores = [0.5] * len(chunks)

    arr = np.array(chunk_scores)

    return {
        "score": round(float(np.mean(arr)), 3),
        "per_chunk": [round(s, 3) for s in chunk_scores],
        "detail": {
            "max_chunk_score": round(float(np.max(arr)), 3),
            "min_chunk_score": round(float(np.min(arr)), 3),
            "score_variance": round(float(np.var(arr)), 4),
            "chunks_analyzed": len(chunk_scores),
            "ai_label_index": _ai_label_idx,
        },
    }
