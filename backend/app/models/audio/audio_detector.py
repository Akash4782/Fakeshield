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
    
    # Step 2 & 3: Run Sequential ML and DSP pipelines CONCURRENTLY
    print("Dispatching Parallel Signal Analyzers (WavLM, AST, Speaker, Prosody, Spectral, Robustness)...")
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=7) as executor:
        f_wlm = executor.submit(signal_wavlm, audio.chunks)
        f_w2v = executor.submit(signal_wav2vec, audio.chunks)
        f_spk = executor.submit(signal_speaker_consistency, audio.waveform, audio.sr, audio.chunks)
        f_pros = executor.submit(signal_prosody, audio.waveform, audio.sr, audio.chunks)
        f_spec = executor.submit(signal_spectral, audio.waveform, audio.sr, audio.chunks)
        f_codec = executor.submit(signal_codec_artifacts, audio.waveform, audio.sr)
        
        # Robustness Check also dispatched concurrently
        def wlm_scoring_pass(y, sr):
            # Speed over breath for robustness check
            y_sample = y[:int(sr*8)] # 8s instead of 12s
            tmp_chunks = [y_sample[i:i+int(sr*4)] for i in range(0, len(y_sample), int(sr*4))]
            return signal_wavlm(tmp_chunks).get("score", 0.5)
            
        f_robust = executor.submit(analyze_robustness, audio.waveform, audio.sr, wlm_scoring_pass)
        
        # Collect parallel results
        wlm_result = f_wlm.result()
        w2v_result = f_w2v.result()
        spk_result = f_spk.result()
        pros_result = f_pros.result()
        spec_result = f_spec.result()
        codec_result = f_codec.result()
        robustness = f_robust.result()

    
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
