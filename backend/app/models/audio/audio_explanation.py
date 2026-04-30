# audio_explanation.py
from dataclasses import dataclass


@dataclass
class AudioReason:
    signal:   str
    severity: str
    message:  str
    evidence: str
    score:    float


def generate_audio_explanation_v1(
    signals: dict,
    verdict: str,
    ai_probability: float,
    audio_meta: dict,
    robustness: dict,
) -> dict:
    primary:    list[AudioReason] = []
    supporting: list[AudioReason] = []
    exonerating: list[str] = []
    
    # Extract scores
    s_wavlm   = signals["wavlm"]["score"]
    s_wav2vec = signals["wav2vec"]["score"]
    s_prosody = signals["prosody"]["score"]
    s_speaker = signals["speaker"]["score"]
    s_spec    = signals["spectral"]["score"]
    s_codec   = signals["codec"]["score"]
    
    # Extract details
    d_wavlm   = signals["wavlm"].get("detail", {})
    d_prosody = signals["prosody"].get("detail", {})
    d_speaker = signals["speaker"].get("detail", {})
    d_spec    = signals["spectral"].get("detail", {})
    d_codec   = signals["codec"].get("detail", {})
    
    stability_score = robustness.get("stability_score", 1.0)
    
    # --- 1. PRIMARY SSL MODELS ---
    if s_wavlm >= 0.85:
        primary.append(AudioReason("wavlm", "critical",
            "WavLM-ITW identifies sophisticated voice synthesis artifacts",
            f"Confidence {s_wavlm:.1%}", s_wavlm))
    elif s_wavlm >= 0.65:
        supporting.append(AudioReason("wavlm", "high",
            "Speech patterns match neural synthesis profiles",
            f"In-the-wild classifier score {s_wavlm:.1%}", s_wavlm))
            
    if s_wav2vec >= 0.80:
        supporting.append(AudioReason("wav2vec", "high",
            "Supplemental SSL model detects deepfake characteristics",
            f"Wav2Vec2 score {s_wav2vec:.1%}", s_wav2vec))

    # --- 2. PROSODY (LINGUISTIC) ---
    f0_std = d_prosody.get("f0_std_semitones", 2.5)
    ioi_cv = d_prosody.get("rhythm_ioi_cv", 0.3)
    
    if s_prosody >= 0.70:
        msg = "Prosody is unnaturally regular"
        if f0_std < 1.5: msg = "Robotic pitch monotony detected"
        elif ioi_cv < 0.18: msg = "Metronomic speech rhythm detected"
        
        supporting.append(AudioReason("prosody", "high", msg,
            f"Pitch std: {f0_std:.2f} semitones; Rhythm CV: {ioi_cv:.3f}", s_prosody))
    elif s_prosody < 0.30:
        exonerating.append("Natural prosodic variation — pitch and rhythm match human speech")

    # --- 3. SPEAKER IDENTITY ---
    if s_speaker >= 0.75:
        reason = "Voice identity inconsistency"
        if d_speaker.get("is_unnatural_constancy"):
            reason = "Unnatural identity stability (over-consistent voice clone)"
        elif d_speaker.get("is_identity_drift"):
            reason = "Identity drift detected — characteristic of voice conversion"
            
        primary.append(AudioReason("speaker", "high", reason,
            f"Identity stability std: {d_speaker.get('std_sim', 0):.4f}", s_speaker))
    elif s_speaker < 0.30:
        exonerating.append("Speaker identity is stable with natural variation throughout")

    # --- 4. ROBUSTNESS & STABILITY ---
    if stability_score < 0.75:
        supporting.append(AudioReason("stability", "medium",
            "Detection is unstable under compression/resampling",
            f"Stability score {stability_score:.2f} (Suspicious: Real audio is more stable)", 0.6))
    else:
        exonerating.append(f"Detection is highly stable across multiple robustness passes ({stability_score:.2f})")

    # --- 5. SPECTRAL/CODEC ---
    if s_spec >= 0.75:
        supporting.append(AudioReason("spectral", "medium",
            "Spectral artifacts consistent with neural vocoder synthesis",
            f"Frequency cutoff/smoothing detected", s_spec))

    # Final summary construction
    strong_ai = sum(1 for s in [s_wavlm, s_wav2vec, s_prosody, s_speaker] if s >= 0.65)
    confidence = "HIGH" if (strong_ai >= 3 and stability_score > 0.8) else "MEDIUM" if strong_ai >= 2 else "LOW"
    
    summary = f"Analysis of {audio_meta.get('duration_sec', 0):.1f}s audio. "
    if primary:
        summary += f"Found critical indicators: {primary[0].message}. "
    if not robustness.get("is_stable"):
        summary += "Note: Analysis results showed instability under stress-testing."

    return {
        "forensic_summary":    summary,
        "recommended_action":  _recommended_action_v1(verdict, confidence),
        "confidence":          confidence,
        "stability_report":    robustness,
        "primary_reasons":     [_reason_dict_v1(r) for r in sorted(primary, key=lambda r: r.score, reverse=True)],
        "supporting_reasons":  [_reason_dict_v1(r) for r in sorted(supporting, key=lambda r: r.score, reverse=True)],
        "exonerating_factors": exonerating,
    }


def _reason_dict_v1(r: AudioReason) -> dict:
    return {"signal": r.signal, "severity": r.severity,
            "message": r.message, "evidence": r.evidence, "score": r.score}


def _recommended_action_v1(verdict: str, confidence: str) -> str:
    table = {
        ("AI_GENERATED", "HIGH"):   "Do not use as authentic voice evidence. Flag for immediate fraud review.",
        ("AI_GENERATED", "MEDIUM"): "Strong indicators of synthesis. Verify via independent channels.",
        ("LIKELY_AI",    "HIGH"):   "Highly suspicious. Treat as untrusted.",
        ("UNCERTAIN",    "MEDIUM"): "Inconclusive result due to signal instability or noise.",
        ("LIKELY_HUMAN", "HIGH"):   "Audio appears authentic. Documented stability is high.",
    }
    return table.get((verdict, confidence), "Independent forensic review recommended for critical decisions.")
