# signal_prosody.py
"""
Signal 3: Prosody and rhythm analysis.

AI-synthesized speech has unnatural prosodic characteristics:
- Pitch variance too low (robotic monotone) OR too perfect (over-expressive TTS)
- Pause distribution too regular (uniform timing between words)
- Rhythm too metronomic — syllable durations cluster near mean
- Missing micro-variations in speaking rate

All features normalized — thresholds are unitless and calibration-stable.
"""
import numpy as np
import librosa
import concurrent.futures
from scipy.signal import find_peaks
from scipy.stats import kurtosis, skew


def signal_prosody(waveform: np.ndarray, sr: int, chunks: list) -> dict:
    """
    Full prosody analysis on waveform.
    """
    if len(waveform) < sr * 1.0:
        return {"score": 0.5, "per_chunk": [], "detail": {"reason": "too short"}}
    
    features = _extract_prosody_features(waveform, sr)
    global_score = _score_prosody(features)
    
    # Parallelize chunk analysis (Significant 5x-10x speedup for pyin)
    with concurrent.futures.ThreadPoolExecutor(max_workers=min(len(chunks), 8)) as executor:
        def process_chunk(chunk):
            try:
                f = _extract_prosody_features(chunk, sr)
                return _score_prosody(f)
            except Exception:
                return 0.5
        
        chunk_scores = list(executor.map(process_chunk, chunks))
    
    return {
        "score": round(max(0.0, min(1.0, global_score)), 3),
        "per_chunk": [round(s, 3) for s in chunk_scores],
        "detail": features,
    }


def _extract_prosody_features(y: np.ndarray, sr: int) -> dict:
    
    # --- Fundamental frequency (F0) extraction ---
    # Use pyin — more accurate than piptrack for prosody analysis
    f0, voiced_flag, voiced_probs = librosa.pyin(
        y,
        fmin=librosa.note_to_hz("C2"),   # ~65Hz
        fmax=librosa.note_to_hz("C7"),   # ~2093Hz
        sr=sr,
        frame_length=2048,
    )
    
    # Use only voiced frames
    voiced_f0 = f0[voiced_flag & ~np.isnan(f0)]
    
    if len(voiced_f0) < 10:
        return _empty_prosody_features()
    
    # Normalize F0 to semitones (log scale — perceptually meaningful)
    # This makes variance stable across speakers
    f0_semitones = 12 * np.log2(voiced_f0 / (np.median(voiced_f0) + 1e-10) + 1e-10)
    
    f0_std = float(np.std(f0_semitones))       # variance in semitones
    f0_range = float(np.max(f0_semitones) - np.min(f0_semitones))
    f0_kurtosis = float(kurtosis(f0_semitones))  # peakedness of distribution
    
    # --- Rhythm: energy envelope regularity ---
    # Compute short-time energy
    hop = int(sr * 0.010)
    energy = np.array([
        np.sum(y[i:i+hop]**2)
        for i in range(0, len(y) - hop, hop)
    ])
    energy_norm = energy / (energy.max() + 1e-10)
    
    # Find energy peaks (syllable onsets)
    peaks, _ = find_peaks(energy_norm, height=0.1, distance=int(0.1 * sr / hop))
    
    if len(peaks) < 4:
        ioi_cv = 0.5  # can't measure rhythm
        ioi_mean = 0.0
    else:
        # Inter-onset intervals
        ioi = np.diff(peaks).astype(float) * hop / sr  # in seconds
        ioi_mean = float(np.mean(ioi))
        ioi_std = float(np.std(ioi))
        # CV (coefficient of variation) — normalized variability
        ioi_cv = ioi_std / (ioi_mean + 1e-10)
    
    # --- Pause analysis ---
    # Real speech: irregular pauses. AI: regular, minimal pauses.
    silence_threshold = float(np.mean(energy_norm)) * 0.05
    is_silent = energy_norm < silence_threshold
    
    # Count pause durations
    pauses = []
    in_pause = False
    pause_start = 0
    
    for i, silent in enumerate(is_silent):
        if silent and not in_pause:
            pause_start = i
            in_pause = True
        elif not silent and in_pause:
            pause_dur = (i - pause_start) * hop / sr
            if pause_dur > 0.05:  # ignore <50ms pauses
                pauses.append(pause_dur)
            in_pause = False
    
    pause_cv = 0.5
    if len(pauses) >= 3:
        p_arr = np.array(pauses)
        pause_cv = float(np.std(p_arr) / (np.mean(p_arr) + 1e-10))
    
    # --- Speaking rate variance ---
    # Real speech: speaking rate changes naturally
    # Window: 1-second chunks, count energy peaks per window
    window_peaks = []
    window_size = int(sr / hop)
    for i in range(0, len(energy_norm) - window_size, window_size // 2):
        window = energy_norm[i:i + window_size]
        wpeaks, _ = find_peaks(window, height=0.1)
        window_peaks.append(len(wpeaks))
    
    rate_variance = float(np.var(window_peaks)) if len(window_peaks) > 2 else 0.5
    
    return {
        "f0_std_semitones": round(f0_std, 3),
        "f0_range_semitones": round(f0_range, 3),
        "f0_kurtosis": round(f0_kurtosis, 3),
        "rhythm_ioi_cv": round(ioi_cv, 3),
        "pause_cv": round(pause_cv, 3),
        "speaking_rate_variance": round(rate_variance, 3),
        "voiced_frame_count": len(voiced_f0),
    }


def _score_prosody(f: dict) -> float:
    """
    Convert prosody features to AI probability.
    
    Calibrated on ASVspoof + VCTK natural speech comparison:
    - F0 std in semitones: real ~2.5–5.0, TTS ~0.5–1.8 (monotone) or >7 (over-expressive)
    - IOI CV (rhythm): real ~0.25–0.55, TTS ~0.05–0.18 (metronomic)
    - Pause CV: real ~0.40–0.80, TTS ~0.05–0.25 (uniform pauses)
    """
    sub_scores = []
    
    # F0 variance — too low (monotone TTS) OR too high (over-expressive TTS)
    f0_std = f.get("f0_std_semitones", 2.5)
    if f0_std < 0.3:
        f0_score = 0.90  # silent / very monotone
    elif f0_std < 1.5:
        f0_score = 0.75  # unnaturally flat
    elif f0_std > 8.0:
        f0_score = 0.60  # over-expressive (some TTS overcorrects)
    else:
        # Natural range 1.5–8.0 → score from 0.1 to 0.4
        f0_score = max(0.10, 0.40 - (f0_std - 1.5) / 13.0)
    sub_scores.append((f0_score, 0.35))
    
    # Rhythm regularity — too regular = AI
    ioi_cv = f.get("rhythm_ioi_cv", 0.3)
    rhythm_score = 1.0 - min(1.0, max(0.0, (ioi_cv - 0.03) / 0.45))
    sub_scores.append((rhythm_score, 0.30))
    
    # Pause regularity — too regular = AI
    pause_cv = f.get("pause_cv", 0.3)
    pause_score = 1.0 - min(1.0, max(0.0, (pause_cv - 0.05) / 0.65))
    sub_scores.append((pause_score, 0.20))
    
    # Speaking rate variance — too constant = AI
    rate_var = f.get("speaking_rate_variance", 1.0)
    rate_score = 1.0 - min(1.0, max(0.0, rate_var / 8.0))
    sub_scores.append((rate_score, 0.15))
    
    total_w = sum(w for _, w in sub_scores)
    return sum(s * w for s, w in sub_scores) / total_w


def _empty_prosody_features() -> dict:
    return {
        "f0_std_semitones": 2.5,
        "f0_range_semitones": 5.0,
        "f0_kurtosis": 0.0,
        "rhythm_ioi_cv": 0.3,
        "pause_cv": 0.3,
        "speaking_rate_variance": 1.0,
        "voiced_frame_count": 0,
    }
