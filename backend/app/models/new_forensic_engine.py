"""
FakeShield — Vanguard Forensic Engine v60.0 (The Sovereign Vanguard)
============================================================
The 'Vanguard' wrapper ensures high-performance forensic analysis
for the Text Lab, providing sentence-level explainability and 
adversarial robustness against humanized AI text.
"""

import time
from typing import Dict, Any

def load_models():
    """Warmup function called by main.py."""
    from app.models.text_classifier_ensemble import load_vanguard_v85
    load_vanguard_v85()

def analyze_forensic(text: str, mode: str = "vanguard") -> Dict[str, Any]:
    """
    Main entry point for Vanguard Engine v60.0.
    Delivers 2026-grade forensic accuracy and explainability.
    """
    from app.models.text_classifier_ensemble import ensemble_predict
    
    t0 = time.time()
    
    # 1. Execution
    result = ensemble_predict(text, mode=mode)
    
    # 2. Enrichment for SaaS UI
    result["processing_time"] = f"{round(time.time() - t0, 2)}s"
    result["engine_tier"] = "VANGUARD-SOVEREIGN"
    result["score"] = result.get("overall_score", 0.5)
    
    return result
