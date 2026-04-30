# audio_fusion.py
"""
Hierarchical Fusion Engine for FakeShield Audio Lab v1.0.

Core Principle: Detection is a decision tree, not a simple average.
- Prioritize strong model agreement.
- Catch cross-signal inconsistencies.
- Default to Real if evidence is weak.
"""
import numpy as np


def fuse_audio_signals_v1(
    wavlm: dict,
    wav2vec: dict,
    prosody: dict,
    speaker: dict,
    spectral: dict,
    codec: dict,
    robustness: dict,
) -> dict:
    
    s_wavlm   = wavlm.get("score", 0.5)
    s_wav2vec = wav2vec.get("score", 0.5)
    s_prosody = prosody.get("score", 0.5)
    s_speaker = speaker.get("score", 0.5)
    s_spec    = spectral.get("score", 0.5)
    s_codec   = codec.get("score", 0.5)
    
    stability = robustness.get("stability_score", 1.0)
    
    all_scores = [s_wavlm, s_wav2vec, s_prosody, s_speaker, s_spec, s_codec]
    
    # --- PHASE 1: STRONG AI SIGNALS (High Confidence) ---
    
    # Agreement between primary SSL models
    if s_wavlm >= 0.85 and s_wav2vec >= 0.80:
        return _result(0.92, "STRONG_SSL_AGREEMENT", "AI_GENERATED")
    
    # WavLM is very confident and one other signal agrees
    if s_wavlm >= 0.88 and any(s >= 0.65 for s in [s_prosody, s_speaker]):
        return _result(s_wavlm, "WAVLM_SUPPORTED", "AI_GENERATED")

    # --- PHASE 2: CROSS-SIGNAL INCONSISTENCY (Linguistic/Identity) ---
    
    # Multimodal mismatch: identity drift/flatness + unnatural rhythm
    if s_speaker >= 0.75 and s_prosody >= 0.70:
        fused = (s_speaker + s_prosody) / 2.0
        return _result(fused, "MULTIMODAL_INCONSISTENCY", "LIKELY_AI")
    
    # --- PHASE 3: STABILITY & UNCERTAINTY ---
    
    if stability < 0.60:
        # If the detection is highly unstable across compressions, mark uncertain
        # unless primary signals are near-perfect
        if s_wavlm < 0.92:
            return _result(max(0.45, np.mean(all_scores)), "UNSTABLE_DETECTION", "UNCERTAIN")

    # --- PHASE 4: ADAPTIVE WEIGHTED BLEND ---
    
    weights = {
        "wavlm":    0.40,
        "wav2vec":  0.20,
        "prosody":  0.15,
        "speaker":  0.15,
        "spectral": 0.05,
        "codec":    0.05,
    }
    
    fused = sum(weights[k] * s for k, s in zip(weights.keys(), all_scores))
    
    # --- PHASE 5: REAL AUDIO PROTECTION (The Default) ---
    
    # If no signal passes 0.60 threshold, bias heavily towards real
    if all(s < 0.60 for s in all_scores):
        fused = min(fused, 0.35)
        return _result(fused, "NO_STRONG_AI_EVIDENCE", "LIKELY_HUMAN")
        
    # Final verdict mapping
    if fused >= 0.80: return _result(fused, "WEIGHTED_BLEND", "AI_GENERATED")
    if fused >= 0.55: return _result(fused, "WEIGHTED_BLEND", "LIKELY_AI")
    if fused >= 0.48: return _result(fused, "WEIGHTED_BLEND", "UNCERTAIN")
    
    return _result(fused, "WEIGHTED_BLEND", "LIKELY_HUMAN")


def _result(score: float, rule: str, verdict: str) -> dict:
    score = max(0.0, min(1.0, score))
    
    threat = {
        "AI_GENERATED": "CRITICAL",
        "LIKELY_AI":    "HIGH",
        "UNCERTAIN":     "MEDIUM",
        "LIKELY_HUMAN":  "LOW",
    }.get(verdict, "LOW")
    
    return {
        "ai_probability": round(score * 100, 1),
        "verdict":        verdict,
        "threat_level":   threat,
        "fusion_rule":    rule,
    }
