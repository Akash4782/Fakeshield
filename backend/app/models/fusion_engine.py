"""
FakeShield Fusion Engine v13.0 — Ensemble Pass-Through
=======================================================
The new v13.0 forensic engine doesn't use the behavioral fusion model anymore.
The ensemble (HC3 + GPT2 + Binoculars) computes probability directly.

This module is kept for backward compatibility if any legacy code imports it.
"""

import numpy as np


class FusionEngine:
    """
    Legacy stub. v13.0 uses text_classifier_ensemble.py directly.
    This is only called if legacy code paths are used.
    """

    def __init__(self):
        self.margin = 0.10

    def fuse(self, signals: dict, word_count: int = 500) -> dict:
        """Simple classifier-anchored pass-through for legacy compatibility."""
        s = {k: float(v) for k, v in signals.items()}

        # Primary signal is the classifier
        primary = s.get("classifier_signal", s.get("hc3_classifier", 0.5))

        # Supporting signals
        ppl     = s.get("ppl_signal", s.get("ppl_uniformity", 0.5))
        burst   = s.get("burstiness_signal", 0.5)
        bino    = s.get("binoculars_signal", 0.5)

        ai_probability = (
            primary * 0.50 +
            ppl     * 0.25 +
            burst   * 0.15 +
            bino    * 0.10
        )
        ai_probability = float(np.clip(ai_probability, 0.0, 1.0))

        if ai_probability >= 0.80:
            verdict, threat = "AI GENERATED", "CRITICAL"
        elif ai_probability >= 0.60:
            verdict, threat = "LIKELY AI", "HIGH"
        elif ai_probability >= 0.45:
            verdict, threat = "UNCERTAIN", "MEDIUM"
        else:
            verdict, threat = "LIKELY HUMAN", "LOW"

        return {
            "ai_probability":    round(ai_probability, 4),
            "verdict":           verdict,
            "threat_level":      threat,
            "confidence":        "HIGH" if ai_probability < 0.40 or ai_probability > 0.65 else "MEDIUM",
            "rule_applied":      "Ensemble Pass-Through v13.0",
            "requires_llm":      0.40 <= ai_probability <= 0.65,
            "human_score_raw":   round(1.0 - ai_probability, 4),
            "ai_score_raw":      round(ai_probability, 4),
            "disagreement_factor": 0.0,
        }
