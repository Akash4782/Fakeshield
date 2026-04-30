import sys
import os

# Add parent directory to path to import app.models.image_detector
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.app.models.image_detector import adaptive_ensemble

def test_veto():
    # User's sample data (Xiaomi 2201117TI False Positive case)
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
    
    print("Testing without Veto (old logic Simulation)...")
    # Simulation: metadata weight was 0.03, neural was 0.35, recon 0.40.
    # We can just check the results of the new function with and without meta_data.
    
    print("\n--- Running with Authentic Veto ---")
    result = adaptive_ensemble(signals, c2pa_adj=0.0, meta_data=meta_data)
    
    print(f"Final Probability: {result['prob']:.4f}")
    print(f"Weights Used: {result['weights']}")
    
    if result['prob'] <= 0.65:
        print("\n✅ SUCCESS: Veto applied. Risk score lowered despite high neural/recon signals.")
    else:
        print("\n❌ FAILURE: Veto was not applied or was insufficient.")

if __name__ == "__main__":
    test_veto()
