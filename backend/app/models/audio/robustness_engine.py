# robustness_engine.py
"""
Robustness Engine for FakeShield Audio Lab v1.0.

Industry-level systems MUST be stable under real-world distortions.
Real human voice = stable detection.
AI voice = unstable detection (artifact-based models drift under compression).
"""
import numpy as np
import librosa
from scipy import signal as scipy_signal


def analyze_robustness(waveform: np.ndarray, sr: int, analyze_fn) -> dict:
    """
    Run multi-pass analysis on the audio.
    """
    # CRITICAL OPTIMIZATION: Truncate to 15s for stability check.
    # Resampling large buffers on CPU is extremely slow.
    max_samples = 15 * sr
    waveform = waveform[:max_samples]
    
    # 1. Original Pass
    score_orig = analyze_fn(waveform, sr)
    
    # 2. Resampled Pass (Telephony simulation)
    # 8kHz is THE standard for capturing AI artifacts in telephony
    # Use kaiser_fast for CPU optimization
    y_8k = librosa.resample(waveform, orig_sr=sr, target_sr=8000, res_type='kaiser_fast')
    y_telephony = librosa.resample(y_8k, orig_sr=8000, target_sr=16000, res_type='kaiser_fast')
    score_telephony = analyze_fn(y_telephony, 16000)
    
    # 3. Compute Stability
    all_scores = np.array([score_orig, score_telephony])
    max_delta = float(np.max(all_scores) - np.min(all_scores))
    
    # Stability Score: 1.0 (Stable) to 0.0 (Unstable)
    stability = 1.0 - min(1.0, max_delta / 0.40) # 0.40 delta = 0 stability
    
    return {
        "stability_score": round(stability, 3),
        "is_stable": stability >= 0.70, # tuned for CPU 2-pass
        "scores": {
            "original": round(score_orig, 3),
            "telephony": round(score_telephony, 3),
        },
        "max_delta": round(max_delta, 3),
    }
