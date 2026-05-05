import json
import time
import requests
from typing import List, Dict

# Direct model import for zero-latency testing
from app.models.text_classifier_ensemble import ensemble_predict

# Configuration
# Configuration
DATASET_PATH = "vanguard_adversarial_dataset.json"
OUTPUT_REPORT = "vanguard_adversarial_report.json"

def run_benchmark():
    print("=== FakeShield Vanguard v82.0 — 80 Sample Forensic Audit ===")
    
    # 1. Warmup
    print("[STEP 1] Warming up Vanguard Engine (Neural Anchor, Binoculars, etc.)...")
    ensemble_predict("This is a warmup text to ensure all models are loaded into memory correctly before the benchmark starts. It needs to be at least one hundred words long to pass the forensic gate. Forensic science is the application of scientific methods and techniques to the investigation of crime. It involves the analysis of physical evidence such as fingerprints, DNA, and ballistics. Forensic scientists work in laboratories and at crime scenes to collect and analyze evidence that can be used in court.")
    print("Vanguard Engine ONLINE.\n")
    
    with open(DATASET_PATH, 'r') as f:
        data = json.load(f)
    
    samples = data["samples"]
    total = len(samples)
    results = []
    
    tp, tn, fp, fn = 0, 0, 0, 0
    oracle_count = 0
    
    for i, sample in enumerate(samples):
        print(f"[{i+1}/{total}] Testing: {sample['topic']} ({sample['label']})...", end=" ", flush=True)
        
        try:
            # Direct call to forensic engine
            res_data = ensemble_predict(sample["text"], mode="vanguard")
            
            verdict = res_data["verdict"]
            actual = sample["label"]
            
            # Normalize verdict for comparison
            is_ai_pred = "AI" in verdict and "UNCERTAIN" not in verdict
            is_ai_actual = actual == "AI"
            
            if is_ai_pred and is_ai_actual: tp += 1
            elif not is_ai_pred and not is_ai_actual: tn += 1
            elif is_ai_pred and not is_ai_actual: fp += 1
            elif not is_ai_pred and is_ai_actual: fn += 1
            
            if "ORACLE" in res_data.get("confidence_level", ""):
                oracle_count += 1
                
            results.append({
                "sample": sample,
                "result": res_data,
                "correct": is_ai_pred == is_ai_actual
            })
            
            status_color = "PASS" if is_ai_pred == is_ai_actual else "FAIL"
            print(f"[{status_color}] -> Pred: {verdict} (Score: {res_data['overall_score']})")
            
        except Exception as e:
            print(f"[ERROR] {e}")
            
    # Calculate metrics
    accuracy = (tp + tn) / total
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    
    summary = {
        "metrics": {
            "accuracy": round(accuracy * 100, 2),
            "precision": round(precision * 100, 2),
            "recall": round(recall * 100, 2),
            "f1_score": round(f1, 4)
        },
        "counts": {
            "total": total,
            "tp": tp, "tn": tn, "fp": fp, "fn": fn,
            "oracle_audits": oracle_count
        },
        "details": results
    }
    
    with open(OUTPUT_REPORT, 'w') as f:
        json.dump(summary, f, indent=2)
        
    print("\n" + "="*50)
    print("VANGUARD v80.0 ADVERSARIAL AUDIT COMPLETE")
    print("="*50)
    print(f"ACCURACY:  {summary['metrics']['accuracy']}%")
    print(f"PRECISION: {summary['metrics']['precision']}%")
    print(f"RECALL:    {summary['metrics']['recall']}%")
    print(f"ORACLES:   {summary['counts']['oracle_audits']}")
    print("="*50)

if __name__ == "__main__":
    run_benchmark()
