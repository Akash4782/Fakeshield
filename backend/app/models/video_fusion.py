import numpy as np

class VideoFusionEngine:
    """Ensembles forensic signals with phased reasoning categorization (v11.0)"""
    
    def fuse_signals(self, signals: dict, metadata: dict = None):
        """
        Input: 
          - signals: {k: score}
          - metadata: {"resolution": "1920x1080", "fps": 30, ...}
        """
        metadata = metadata or {}
        res_str = metadata.get("dimensions", "1280x720")
        try:
            h = int(res_str.split('x')[1])
        except:
            h = 720

        # --- Dynamic Multi-Modal Weighting ---
        if h < 480:
            weights = {
                "spatial": 0.20,
                "temporal": 0.20,
                "audio": 0.30,
                "forensic": 0.05,
                "reasoning": 0.25
            }
        elif h >= 1080:
            weights = {
                "spatial": 0.25,
                "temporal": 0.30,
                "audio": 0.15,
                "forensic": 0.20,
                "reasoning": 0.10
            }
        else:
            weights = {
                "spatial": 0.25,
                "temporal": 0.25,
                "audio": 0.20,
                "forensic": 0.15,
                "reasoning": 0.15
            }
        
        available_signals = {k: v for k, v in signals.items() if v is not None}
        total_weight = sum(weights[k] for k in available_signals)
        
        if total_weight == 0:
            return self._empty_response()
            
        # 1. Base Weighted Score
        base_score = sum((signals[k] * weights[k]) for k in available_signals) / total_weight
        
        # 2. Consistency Penalty
        penalty = 0.0
        s_score = signals.get("spatial", 0.5)
        t_score = signals.get("temporal", 0.5)
        if abs(s_score - t_score) > 0.4:
            penalty += 0.1 # High disagreement suggests abnormal cross-modal instability

        ai_prob = float(np.clip(base_score + penalty, 0.0, 1.0))
        
        # --- Categorization ---
        if ai_prob >= 0.75:
            verdict = "AI-Generated"
            threat = "CRITICAL"
        elif ai_prob >= 0.55:
            verdict = "AI-Generated"
            threat = "HIGH"
        elif ai_prob >= 0.35:
            verdict = "Suspicious"
            threat = "MEDIUM"
        else:
            verdict = "Authentic"
            threat = "LOW"
            
        # --- Explainability (Phase 3: Deep Analysis) ---
        reasons = []
        if signals.get("spatial", 0) > 0.65: 
            reasons.append("✓ [Phase 3] Neural artifacts detected in frame texture (Diffusion Signature).")
        if signals.get("temporal", 0) > 0.65: 
            reasons.append("✓ [Phase 3] Physical motion violations: RAFT flow shows temporal morphing.")
        if signals.get("audio", 0) > 0.65: 
            reasons.append("✓ [Phase 3] Phoneme-to-Viseme misalignment: Audio-Lip sync violation.")
        if signals.get("forensic", 0) > 0.65: 
            reasons.append("✓ [Phase 3] Sensor noise anomaly: Spectral fingerprint lacks camera noise.")
        if signals.get("reasoning", 0) > 0.65: 
            reasons.append("✓ [Phase 3] Geometric reasoning identifies physical impossibilities.")
            
        if penalty > 0:
            reasons.append("⚠ High cross-modal instability detected (Spatial/Temporal disagreement).")

        if not reasons:
            if ai_prob > 0.5:
                reasons.append("Overall synthetic probability remains high due to subtle systemic anomalies.")
            else:
                reasons.append("Video maintains high physical and temporal consistency (Authentic Signature).")
        
        return {
            "verdict": verdict,
            "threat_level": threat,
            "ai_probability": ai_prob,
            "confidence": round(ai_prob * 100, 1),
            "agreement_count": f"{sum([1 for s in available_signals.values() if s > 0.5])}/{len(available_signals)}",
            "signals": signals,
            "reasons": reasons,
            "logic_version": "v11.0-PhasedForensics"
        }

    def _empty_response(self):
        return {
            "verdict": "UNCERTAIN",
            "threat_level": "LOW",
            "ai_probability": 0.5,
            "confidence": 50,
            "agreement_count": "0/0",
            "signals": {},
            "reasons": ["Insufficient data for analysis."]
        }
