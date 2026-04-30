import os
import sys
import time
from pathlib import Path

# Add app to path
sys.path.insert(0, str(Path(__file__).parent))
from app.models.image_detector import analyze_image

def run_benchmark():
    real_path = Path("evaluation_dataset/real")
    ai_path = Path("evaluation_dataset/ai")
    
    results = []
    
    print("\n" + "="*50)
    print("  FAKESHIELD v18.1 — BASELINE EVALUATION")
    print("="*50)
    
    # Test REAL images
    print("\n--- Testing REAL images (Expected: REAL) ---")
    for img_path in real_path.glob("*"):
        t0 = time.time()
        try:
            with open(img_path, "rb") as f:
                img_bytes = f.read()
            res = analyze_image(img_bytes)
            elapsed = time.time() - t0
            score = res.get("fake_probability", 0.5)
            verdict = res.get("verdict", "UNKNOWN")
            print(f"  [REAL] {img_path.name:<20} | Score: {score:.1%} | Verdict: {verdict:<12} | Time: {elapsed:.2f}s")
            results.append({"name": img_path.name, "type": "real", "score": score, "verdict": verdict, "correct": verdict == "REAL"})
        except Exception as e:
            print(f"  [ERROR] {img_path.name}: {e}")

    # Test AI images
    print("\n--- Testing AI images (Expected: FAKE) ---")
    for img_path in ai_path.glob("*"):
        t0 = time.time()
        try:
            with open(img_path, "rb") as f:
                img_bytes = f.read()
            res = analyze_image(img_bytes)
            elapsed = time.time() - t0
            score = res.get("fake_probability", 0.5)
            verdict = res.get("verdict", "UNKNOWN")
            print(f"  [AI]   {img_path.name:<20} | Score: {score:.1%} | Verdict: {verdict:<12} | Time: {elapsed:.2f}s")
            results.append({"name": img_path.name, "type": "ai", "score": score, "verdict": verdict, "correct": verdict == "AI_GENERATED" or verdict == "FAKE"})
        except Exception as e:
            print(f"  [ERROR] {img_path.name}: {e}")

    # Summary
    total = len(results)
    correct = sum(1 for r in results if r["correct"])
    accuracy = (correct / total) if total > 0 else 0
    print("\n" + "="*50)
    print(f"  OVERALL ACCURACY: {accuracy:.1%}")
    print("="*50 + "\n")

if __name__ == "__main__":
    run_benchmark()
