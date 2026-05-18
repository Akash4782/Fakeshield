# audio_detector.py
from typing import Dict, Any
from .audio_loader import load_audio
from .signal_wavlm import signal_wavlm
from .signal_wav2vec import signal_wav2vec
from .signal_spectral import signal_spectral
from .signal_prosody import signal_prosody
from .signal_speaker import signal_speaker_consistency
from .signal_codec import signal_codec_artifacts
from .robustness_engine import analyze_robustness
from .audio_fusion import fuse_audio_signals_v1
from .audio_segmentation import build_audio_timeline
from .audio_explanation import generate_audio_explanation_v1
import concurrent.futures


def analyze_audio(audio_bytes: bytes, filename: str = "audio.wav") -> dict:
    import torch
    import librosa
    import numpy as np
    
    # Restrict PyTorch to a single thread to eliminate thread thrashing on CPU
    torch.set_num_threads(1)
    
    # Step 1: Load and Preprocess (Normalize to 16kHz, VAD)
    audio = load_audio(audio_bytes, filename)
    
    if audio.num_chunks == 0:
        return {"error": "No voiced content detected in audio"}
    
    audio_meta = {
        "duration_sec":   audio.duration_sec,
        "num_chunks":     audio.num_chunks,
        "format_hint":    audio.format_hint,
        "file_size_bytes": audio.file_size_bytes,
    }
    
    # Limit standard chunks to 3 chunks (15 seconds) to guarantee sub-3s speed on CPU
    standard_chunks = audio.chunks[:3]
    
    # Telephony simulation for robustness (resample first chunk to 8kHz and back to 16kHz)
    if standard_chunks:
        first_chunk = standard_chunks[0]
        y_8k = librosa.resample(first_chunk, orig_sr=16000, target_sr=8000, res_type='kaiser_fast')
        telephony_chunk = librosa.resample(y_8k, orig_sr=8000, target_sr=16000, res_type='kaiser_fast')
        wlm_chunks = standard_chunks + [telephony_chunk]
    else:
        wlm_chunks = []
    
    # Step 2 & 3: Run Sequential ML and DSP pipelines CONCURRENTLY
    print("Dispatching Parallel Signal Analyzers (WavLM, AST, Speaker, Prosody, Spectral, Robustness)...")
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
        f_wlm = executor.submit(signal_wavlm, wlm_chunks)
        f_w2v = executor.submit(signal_wav2vec, standard_chunks)
        f_spk = executor.submit(signal_speaker_consistency, audio.waveform, audio.sr, standard_chunks)
        f_pros = executor.submit(signal_prosody, audio.waveform, audio.sr, standard_chunks)
        f_spec = executor.submit(signal_spectral, audio.waveform, audio.sr, standard_chunks)
        f_codec = executor.submit(signal_codec_artifacts, audio.waveform, audio.sr)
        
        # Collect parallel results
        wlm_result_raw = f_wlm.result()
        w2v_result = f_w2v.result()
        spk_result = f_spk.result()
        pros_result = f_pros.result()
        spec_result = f_spec.result()
        codec_result = f_codec.result()

    # Parse batched WavLM results to extract original chunks vs telephony chunk
    wlm_per_chunk_raw = wlm_result_raw.get("per_chunk", [])
    if len(wlm_per_chunk_raw) > len(standard_chunks):
        wlm_orig_scores = wlm_per_chunk_raw[:len(standard_chunks)]
        wlm_telephony_score = wlm_per_chunk_raw[-1]
    else:
        wlm_orig_scores = wlm_per_chunk_raw
        wlm_telephony_score = 0.5

    wlm_arr = np.array(wlm_orig_scores) if wlm_orig_scores else np.array([0.5])
    wlm_result = {
        "score": round(float(np.mean(wlm_arr)), 3),
        "per_chunk": [round(s, 3) for s in wlm_orig_scores],
        "detail": {
            "max": round(float(np.max(wlm_arr)), 3),
            "var": round(float(np.var(wlm_arr)), 4),
            "model": "wavlm-itw",
        },
    }

    # Calculate stability score directly from single batched inference
    score_orig = wlm_orig_scores[0] if wlm_orig_scores else 0.5
    score_telephony = wlm_telephony_score
    max_delta = abs(score_orig - score_telephony)
    
    stability = 1.0 - min(1.0, max_delta / 0.40)
    robustness = {
        "stability_score": round(stability, 3),
        "is_stable": stability >= 0.70,
        "scores": {
            "original": round(score_orig, 3),
            "telephony": round(score_telephony, 3),
        },
        "max_delta": round(max_delta, 3),
    }

    
    # Step 4: Hierarchical Fusion
    signals = {
        "wavlm":    wlm_result,
        "wav2vec":  w2v_result,
        "prosody":  pros_result,
        "speaker":  spk_result,
        "spectral": spec_result,
        "codec":    codec_result,
    }
    
    fusion = fuse_audio_signals_v1(
        wavlm=wlm_result,
        wav2vec=w2v_result,
        prosody=pros_result,
        speaker=spk_result,
        spectral=spec_result,
        codec=codec_result,
        robustness=robustness,
    )
    
    # Step 5: Timeline (Temporal Map)
    timeline = build_audio_timeline(
        wav2vec_chunks=wlm_result.get("per_chunk", []), # use primary WLM for timeline
        spectral_chunks=spec_result.get("per_chunk", []),
        prosody_chunks=pros_result.get("per_chunk", []),
        speaker_chunks=spk_result.get("per_chunk", []),
        chunk_times=audio.chunk_times,
    )
    
    # Step 6: Startup-Level Explainability
    explanation = generate_audio_explanation_v1(
        signals=signals,
        verdict=fusion["verdict"],
        ai_probability=fusion["ai_probability"],
        audio_meta=audio_meta,
        robustness=robustness,
    )
    
    # Step 7: Agreement Calculation
    all_scores = [wlm_result["score"], w2v_result["score"], pros_result["score"], 
                  spk_result["score"], spec_result["score"], codec_result["score"]]
    high_conf = sum(1 for s in all_scores if s >= 0.70)
    agreement = f"{high_conf}/{len(all_scores)} models agree"
    
    return {
        **fusion,
        **explanation,
        "audio_metadata": audio_meta,
        "timeline": timeline,
        "stability_score": robustness["stability_score"],
        "agreement": agreement,
        "signal_scores": {
            "wavlm":    round(wlm_result["score"]   * 100, 1),
            "wav2vec":  round(w2v_result["score"]   * 100, 1),
            "prosody":  round(pros_result["score"]  * 100, 1),
            "speaker":  round(spk_result["score"]   * 100, 1),
            "spectral": round(spec_result["score"]  * 100, 1),
            "codec":    round(codec_result["score"] * 100, 1),
        },
        "signal_details": {
            "wavlm":    wlm_result.get("detail", {}),
            "wav2vec":  w2v_result.get("detail", {}),
            "prosody":  pros_result.get("detail", {}),
            "speaker":  spk_result.get("detail", {}),
            "spectral": spec_result.get("detail", {}),
            "codec":    codec_result.get("detail", {}),
        }
    }
