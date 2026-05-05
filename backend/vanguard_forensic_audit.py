import json
import time
import os
import sys
from app.models.text_classifier_ensemble import ensemble_predict

def run_audit():
    print("=== FakeShield Vanguard v82.0 — Production Forensic Audit ===")
    
    # Load dataset
    dataset_path = "vanguard_adversarial_dataset.json"
    if not os.path.exists(dataset_path):
        print(f"ERROR: Dataset not found at {dataset_path}")
        return

    with open(dataset_path, "r") as f:
        data = json.load(f)
        samples = data["samples"]

    print(f"[AUDIT] Loaded {len(samples)} adversarial samples.")
    print("[AUDIT] Initializing Vanguard Forensic Engine (Warmup)...")
    
    # Warmup with first sample
    _ = ensemble_predict(samples[0]["text"])
    print("[AUDIT] Engine ONLINE. Beginning Forensic Sweep...\n")

    results = {
        "true_positives": 0,  # AI correctly identified as AI
        "true_negatives": 0,  # Human correctly identified as Human
        "false_positives": 0, # Human incorrectly identified as AI
        "false_negatives": 0, # AI incorrectly identified as Human
        "insufficient": 0
    }

    start_time = time.time()

    for i, sample in enumerate(samples):
        label = sample["label"]
        text = sample["text"]
        topic = sample["topic"]
        
        # Run prediction
        prediction = ensemble_predict(text)
        verdict = prediction["verdict"]
        score = prediction["overall_score"]

        # Log progress every 5 samples
        if (i + 1) % 5 == 0:
            print(f"  Processed {i+1}/{len(samples)} samples...")

        if verdict == "INSUFFICIENT TEXT":
            results["insufficient"] += 1
            continue

        if label == "AI":
            if verdict == "AI GENERATED":
                results["true_positives"] += 1
            else:
                results["false_negatives"] += 1
                print(f"  [MISS] AI sample on '{topic}' identified as {verdict} (Score: {score:.4f})")
        else: # Human
            if verdict == "HUMAN WRITTEN":
                results["true_negatives"] += 1
            else:
                results["false_positives"] += 1
                print(f"  [FALSE POSITIVE] Human sample on '{topic}' identified as {verdict} (Score: {score:.4f})")

    end_time = time.time()
    total_time = end_time - start_time
    valid_samples = len(samples) - results["insufficient"]

    # Calculate Metrics
    tp = results["true_positives"]
    tn = results["true_negatives"]
    fp = results["false_positives"]
    fn = results["false_negatives"]

    accuracy = (tp + tn) / valid_samples if valid_samples > 0 else 0
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

    print("\n" + "="*50)
    print("VANGUARD FORENSIC AUDIT RESULTS")
    print("="*50)
    print(f"Total Samples:    {len(samples)}")
    print(f"Valid Samples:    {valid_samples}")
    print(f"Insufficient:     {results['insufficient']}")
    print("-" * 20)
    print(f"True Positives:   {tp}")
    print(f"True Negatives:   {tn}")
    print(f"False Positives:  {fp}")
    print(f"False Negatives:  {fn}")
    print("-" * 20)
    print(f"ACCURACY:         {accuracy*100:.2f}%")
    print(f"PRECISION:        {precision*100:.2f}%")
    print(f"RECALL:           {recall*100:.2f}%")
    print(f"F1-SCORE:         {f1:.4f}")
    print("-" * 20)
    print(f"Execution Time:   {total_time:.2f}s ({total_time/valid_samples:.2f}s/sample)")
    print("="*50)

    # Save report
    report = {
        "metrics": {
            "accuracy": accuracy,
            "precision": precision,
            "recall": recall,
            "f1_score": f1
        },
        "counts": results,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }
    with open("vanguard_audit_report.json", "w") as f:
        json.dump(report, f, indent=4)
    
    print("\nSUCCESS: Forensic audit complete. Report saved to vanguard_audit_report.json")

if __name__ == "__main__":
    run_audit()
