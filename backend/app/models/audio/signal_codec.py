# signal_codec.py
"""
Signal 5: Compression and codec artifact analysis.

AI-generated audio often shows:
- Resampling artifacts (spectral ripple from integer-ratio resampling)
- Missing dithering noise (synthetic audio lacks analog noise floor)
- Abnormal DC offset patterns (TTS synthesizers leave characteristic offsets)
- ENF (Electrical Network Frequency) absence — real recordings pick up 50/60Hz mains hum
- Quantization artifacts from vocoder output

These are low-level forensic signals — individually weak, but in ensemble they help.
"""
import numpy as np
import librosa
from scipy import signal as scipy_signal


def signal_codec_artifacts(waveform: np.ndarray, sr: int) -> dict:
    """
    Low-level codec and synthesis artifact detection.
    """
    features = {}
    sub_scores = []
    
    # --- 1. Noise floor analysis ---
    # Real recordings have a natural noise floor from microphone/ADC
    # Pure TTS audio: extremely low noise floor, no analog noise
    # Use the quietest 5% of frames as noise floor estimate
    hop = int(sr * 0.020)
    energy = np.array([
        np.sum(waveform[i:i+hop]**2)
        for i in range(0, len(waveform) - hop, hop)
    ])
    
    # Noise floor: 5th percentile energy
    noise_floor = float(np.percentile(energy, 5))
    signal_energy = float(np.percentile(energy, 75))
    
    # SNR proxy (dB)
    snr_proxy = 10 * np.log10(signal_energy / (noise_floor + 1e-20))
    features["snr_proxy_db"] = round(float(snr_proxy), 2)
    
    # Very high SNR (>60dB) = suspiciously clean = likely TTS
    snr_score = min(1.0, max(0.0, (snr_proxy - 40) / 30.0))
    sub_scores.append((snr_score, 0.25))
    
    # --- 2. DC offset ---
    # Real microphones: mean ~0 (AC-coupled ADC)
    # Some TTS vocoders: small but nonzero DC offset
    dc_offset = float(np.abs(np.mean(waveform)))
    features["dc_offset"] = round(dc_offset, 6)
    
    dc_score = min(1.0, dc_offset / 0.02)
    sub_scores.append((dc_score, 0.15))
    
    # --- 3. Spectral ripple (resampling artifacts) ---
    # When audio is resampled at non-integer ratios, spectral ripple appears
    fft = np.abs(np.fft.rfft(waveform[:sr * 2]))  # first 2 seconds
    fft_norm = fft / (np.mean(fft) + 1e-10)
    
    # Detect periodic ripple using autocorrelation of spectrum
    spec_autocorr = np.correlate(fft_norm[:1000], fft_norm[:1000], mode='full')
    spec_autocorr = spec_autocorr[len(spec_autocorr)//2:]
    
    # Peak at non-zero lag = periodic ripple
    peaks, _ = scipy_signal.find_peaks(spec_autocorr[10:200], height=0.3)
    ripple_score = min(1.0, len(peaks) / 5.0)
    features["spectral_ripple_peaks"] = len(peaks)
    sub_scores.append((ripple_score, 0.20))
    
    # --- 4. ENF (Electrical Network Frequency) presence ---
    # Real indoor recordings usually pick up 50Hz or 60Hz mains hum
    # Pure synthetic audio: no ENF
    freqs = np.fft.rfftfreq(len(waveform[:sr * 4]), d=1/sr)
    fft_4s = np.abs(np.fft.rfft(waveform[:sr * 4]))
    
    # Check for 50Hz and 60Hz peaks
    def find_enf(target_hz, tolerance=2.0):
        mask = np.abs(freqs - target_hz) < tolerance
        if not np.any(mask):
            return 0.0
        peak_energy = float(np.mean(fft_4s[mask]))
        neighbor_mask = (np.abs(freqs - target_hz) > 3) & (np.abs(freqs - target_hz) < 10)
        if not np.any(neighbor_mask):
            return 0.0
        neighbor_energy = float(np.mean(fft_4s[neighbor_mask]))
        return peak_energy / (neighbor_energy + 1e-10)
    
    enf_50 = find_enf(50.0)
    enf_60 = find_enf(60.0)
    enf_strength = max(enf_50, enf_60)
    features["enf_strength"] = round(float(enf_strength), 3)
    
    # No ENF = slight AI signal (but not definitive — some real recordings lack it too)
    enf_score = 0.4 if enf_strength < 1.2 else 0.1
    sub_scores.append((enf_score, 0.15))
    
    # --- 5. Clipping and saturation ---
    # Real recordings sometimes clip. TTS never clips.
    # Very clean audio (no samples near ±1.0) = slight AI signal
    near_clip = float(np.mean(np.abs(waveform) > 0.95))
    features["near_clip_ratio"] = round(near_clip, 5)
    
    clip_score = 0.3 if near_clip < 0.0001 else 0.1
    sub_scores.append((clip_score, 0.10))
    
    # --- 6. Dithering noise signature ---
    # Real ADC quantization adds low-level noise that shows in the lowest bits
    # TTS: quantization noise pattern differs (vocoder output)
    # Estimate as variance of residual after low-pass filter
    b, a = scipy_signal.butter(4, 100 / (sr / 2), btype='low')
    lp = scipy_signal.filtfilt(b, a, waveform)
    residual = waveform - lp
    residual_var = float(np.var(residual))
    features["lp_residual_variance"] = round(residual_var, 8)
    
    # Very low residual = no natural noise = possible TTS
    noise_score = 1.0 - min(1.0, residual_var / 0.0001)
    sub_scores.append((noise_score, 0.15))
    
    # Final score
    total_w = sum(w for _, w in sub_scores)
    final_score = sum(s * w for s, w in sub_scores) / total_w
    
    return {
        "score": round(max(0.0, min(1.0, final_score)), 3),
        "detail": {
            **features,
            "sub_scores": {
                "snr": round(snr_score, 3),
                "dc_offset": round(dc_score, 3),
                "spectral_ripple": round(ripple_score, 3),
                "enf": round(enf_score, 3),
                "clipping": round(clip_score, 3),
                "dithering": round(noise_score, 3),
            }
        }
    }
