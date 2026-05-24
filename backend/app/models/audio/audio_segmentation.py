# audio_segmentation.py
"""
Build per-second timeline from per-chunk signal scores.
This powers the suspicious-segment heatmap in the UI.
"""
import numpy as np


def build_audio_timeline(
    wav2vec_chunks:  list,
    spectral_chunks: list,
    prosody_chunks:  list,
    speaker_chunks:  list,
    chunk_times:     list,
    overall_ai_prob: float = None,
) -> list:
    """
    Fuse per-chunk scores into timeline segments.
    Each entry covers one 5-second chunk.

    BUG FIX: Previously used min() over all list lengths without guarding for
    empty lists, so min(0, 3, 3, 3) = 0 always produced an empty timeline.
    Now handles lists of different lengths gracefully.
    """
    # Determine safe iteration count
    lengths = [
        len(wav2vec_chunks)  if wav2vec_chunks  else 0,
        len(spectral_chunks) if spectral_chunks else 0,
        len(prosody_chunks)  if prosody_chunks  else 0,
        len(chunk_times)     if chunk_times     else 0,
    ]

    # Use max of available signal lengths but cap at chunk_times
    n_times = len(chunk_times) if chunk_times else 0
    n_signals = max(
        len(wav2vec_chunks)  if wav2vec_chunks  else 0,
        len(spectral_chunks) if spectral_chunks else 0,
        len(prosody_chunks)  if prosody_chunks  else 0,
    )

    # n = number of segments we can build (bounded by chunk_times)
    n = n_times if n_times > 0 else 0

    if n == 0:
        return []

    timeline = []

    # Compute global means for smarter fallbacks
    w_mean  = float(np.mean(wav2vec_chunks))  if wav2vec_chunks  else (overall_ai_prob if overall_ai_prob is not None else 0.5)
    sp_mean = float(np.mean(spectral_chunks)) if spectral_chunks else (overall_ai_prob if overall_ai_prob is not None else 0.5)
    pr_mean = float(np.mean(prosody_chunks))  if prosody_chunks  else (overall_ai_prob if overall_ai_prob is not None else 0.5)
    sk_mean = float(np.mean(speaker_chunks))  if speaker_chunks  else (overall_ai_prob if overall_ai_prob is not None else 0.5)

    for i in range(n):
        # Safely access each list with fallback to global means
        w  = float(wav2vec_chunks[i])  if i < len(wav2vec_chunks)  else w_mean
        sp = float(spectral_chunks[i]) if i < len(spectral_chunks) else sp_mean
        pr = float(prosody_chunks[i])  if i < len(prosody_chunks)  else pr_mean
        sk = float(speaker_chunks[i])  if i < len(speaker_chunks)  else sk_mean

        # Weighted chunk score — Weights balanced with fusion engine
        chunk_score = 0.50 * w + 0.10 * sp + 0.20 * pr + 0.20 * sk
        
        # Pull chunk score towards overall probability to prevent UX disconnect
        # We increase the 'pull' for unanalyzed segments to ensure consistency
        if overall_ai_prob is not None:
            is_fallback = (i >= n_signals)
            threshold = 0.05 if is_fallback else 0.15
            if abs(chunk_score - overall_ai_prob) > threshold:
                blend_factor = 0.8 if is_fallback else 0.6
                chunk_score = ((1.0 - blend_factor) * chunk_score) + (blend_factor * overall_ai_prob)

        chunk_score = max(0.0, min(1.0, chunk_score))

        start_t, end_t = chunk_times[i] if i < len(chunk_times) else (i * 5, i * 5 + 5)

        # Calibrated levels matching UI: Authentic (Low), Suspicious (Med), High Risk (High), Synthetic (Crit)
        level = (
            "critical" if chunk_score >= 0.75 else
            "high"     if chunk_score >= 0.55 else
            "medium"   if chunk_score >= 0.38 else
            "low"
        )

        timeline.append({
            "segment":    i + 1,
            "start_sec":  round(float(start_t), 2),
            "end_sec":    round(float(end_t), 2),
            "ai_score":   round(chunk_score * 100, 1),
            "level":      level,
            "signals": {
                "wavlm":    round(w  * 100, 1),
                "wav2vec":  round(w  * 100, 1),
                "spectral": round(sp * 100, 1),
                "prosody":  round(pr * 100, 1),
                "speaker":  round(sk * 100, 1),
                "codec":    10.0,  # no per-chunk codec — static baseline
            },
        })

    return timeline
