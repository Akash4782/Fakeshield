import numpy as np

ENSEMBLE_CONFIG = {
    "weight_reconstruction": 0.40,
    "weight_neural":         0.35,
    "weight_patches":        0.15,
    "weight_noise":          0.07,
    "weight_exif":           0.03,
}

def adaptive_ensemble(signals: dict, c2pa_adj: float = 0.0, meta_data: dict = None) -> dict:
    weights = {
        "reconstruction": ENSEMBLE_CONFIG["weight_reconstruction"],
        "neural":         ENSEMBLE_CONFIG["weight_neural"],
        "patches":        ENSEMBLE_CONFIG["weight_patches"],
        "noise":          ENSEMBLE_CONFIG["weight_noise"],
        "exif":           ENSEMBLE_CONFIG["weight_exif"],
    }
    
    # ── AUTHENTIC VETO: Metadata Priority ───────────────────
    is_real_device = meta_data and (meta_data.get("real_camera") or meta_data.get("has_gps"))
    
    if is_real_device:
        # Boost EXIF weight by 15x and forensic signals by 2x
        weights["exif"] *= 15.0  # 0.03 -> 0.45
        weights["patches"] *= 2.0 # 0.15 -> 0.30
        weights["reconstruction"] *= 0.5 # 0.40 -> 0.20
        weights["neural"] *= 0.4 # 0.35 -> 0.14
        print("[Ensemble] Authentic device detected — Applying Priority Veto")

    confs = {k: 0.30 + (abs(p - 0.50)/0.50)*1.20 for k, p in signals.items()}
    confs["exif"] = min(confs["exif"], 0.40) if not is_real_device else 1.5
    confs["noise"] = min(confs["noise"], 0.60)
    
    tw, ws = 0.0, 0.0
    for k, p in signals.items():
        if k in weights:
            w = weights[k] * confs[k]; ws += w * p; tw += w
    
    final_p = (ws / tw) if tw > 0 else 0.5
    final_p = float(np.clip(final_p + c2pa_adj, 0.0, 1.0))
    
    # Hard Veto Cap: If metadata says REAL, neural cannot push above 65% 
    # unless forensic signals (patches/noise) agree it is a fake.
    if is_real_device and final_p > 0.65:
        forensic_agreement = (signals["patches"] > 0.6 or signals["noise"] > 0.6)
        if not forensic_agreement:
            final_p = 0.45 + (final_p - 0.65) * 0.2 # Force down to ~0.5 range
            print(f"[Ensemble] Veto triggered: Real device signature forced {final_p:.4f}")

    return {"prob": final_p, "weights": weights, "confs": confs}

def test_veto():
    signals = {
        "reconstruction": 0.8118,
        "neural":         0.9997,
        "patches":        0.5364,
        "noise":          0.9,      # legacy texture
        "exif":           0.15
    }
    
    meta_data = {
        "real_camera": True,
        "make": "Xiaomi",
        "model": "2201117TI"
    }
    
    print("--- Running Standalone Veto Test ---")
    result = adaptive_ensemble(signals, c2pa_adj=0.0, meta_data=meta_data)
    
    print(f"Final Probability: {result['prob']:.4f}")
    print(f"Weights Used: {result['weights']}")
    
    if result['prob'] <= 0.65:
        print("\n✅ SUCCESS: Veto applied. Risk score lowered to 0.5 range despite high neural signals.")
    else:
        print(f"\n❌ FAILURE: Veto was not applied or was insufficient. Prob: {result['prob']}")

if __name__ == "__main__":
    test_veto()
