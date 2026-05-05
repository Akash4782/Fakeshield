import os
import sys
import json
import time
from typing import List, Dict, Any

# Add parent dir to path
sys.path.append(os.getcwd())

from app.models.new_forensic_engine import analyze_forensic, load_models

def run_benchmark():
    print("=== FakeShield Titan Engine v50.0 — 80 Sample Benchmark ===")
    
    if not os.path.exists("benchmark_80_samples.json"):
        print("Error: benchmark_80_samples.json not found.")
        return

    with open("benchmark_80_samples.json", "r", encoding="utf-8") as f:
        dataset = json.load(f)

    print("\n[STEP 1] Warming up Titan Engine (Loading DeBERTa, Binoculars, etc.)...")
    load_models()
    print("Titan Engine ONLINE.")

    results = {"human": [], "ai": []}
    
    # Metrics
    tp = 0 # True Positives (AI correctly identified)
    fp = 0 # False Positives (Human incorrectly identified as AI)
    tn = 0 # True Negatives (Human correctly identified)
    fn = 0 # False Negatives (AI incorrectly identified as Human)

    print("\n[STEP 2] Running Forensic Analysis on 40 Human Samples...")
    for i, text in enumerate(dataset["human"]):
        res = analyze_forensic(text)
        is_ai = "AI" in res["verdict"].upper()
        
        if is_ai:
            fp += 1
            results["human"].append({"id": i, "verdict": res["verdict"], "score": res["score"], "status": "FAIL (FP)"})
        else:
            tn += 1
            results["human"].append({"id": i, "verdict": res["verdict"], "score": res["score"], "status": "PASS"})
        
        print(f"  Human {i+1}/40: {res['verdict']} ({res['score']})")

    print("\n[STEP 3] Running Forensic Analysis on 40 AI Samples...")
    for i, text in enumerate(dataset["ai"]):
        res = analyze_forensic(text)
        is_ai = "AI" in res["verdict"].upper()
        
        if is_ai:
            tp += 1
            results["ai"].append({"id": i, "verdict": res["verdict"], "score": res["score"], "status": "PASS"})
        else:
            fn += 1
            results["ai"].append({"id": i, "verdict": res["verdict"], "score": res["score"], "status": "FAIL (FN)"})
        
        print(f"  AI {i+1}/40: {res['verdict']} ({res['score']})")

    # [STEP 4] Calculate Final Metrics
    accuracy = (tp + tn) / 80
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

    print("\n" + "="*50)
    print("TITAN ENGINE v50.0 — BENCHMARK RESULTS")
    print("="*50)
    print(f"Total Samples: 80")
    print(f"True Positives (AI):    {tp}/40")
    print(f"True Negatives (Human): {tn}/40")
    print(f"False Positives:        {fp}/40")
    print(f"False Negatives:        {fn}/40")
    print("-" * 20)
    print(f"ACCURACY:  {accuracy:.2%}")
    print(f"PRECISION: {precision:.2%}")
    print(f"RECALL:    {recall:.2%}")
    print(f"F1-SCORE:  {f1:.4f}")
    print("="*50)

    # Save detailed report
    report = {
        "metrics": {"accuracy": accuracy, "precision": precision, "recall": recall, "f1": f1},
        "confusion_matrix": {"tp": tp, "fp": fp, "tn": tn, "fn": fn},
        "details": results
    }
    with open("titan_benchmark_report.json", "w") as f:
        json.dump(report, f, indent=2)
    print("\nDetailed report saved to titan_benchmark_report.json")

if __name__ == "__main__":
    run_benchmark()
