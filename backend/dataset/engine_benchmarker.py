import os
import sys
import time
import random
import numpy as np
from typing import List, Dict

# Add parent dir to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from app.models.new_forensic_engine import analyze_forensic
except ImportError as e:
    print(f"Import error: {e}")
    sys.exit(1)

class Benchmarker:
    def __init__(self, dataset_path: str):
        self.dataset_path = dataset_path
        self.ai_samples = []
        self.human_samples = []

    def load_dataset(self):
        ai_dir = os.path.join(self.dataset_path, "ai")
        human_dir = os.path.join(self.dataset_path, "human")

        for root, _, files in os.walk(ai_dir):
            for file in files:
                if file.endswith(".txt"):
                    with open(os.path.join(root, file), "r", encoding="utf-8") as f:
                        self.ai_samples.append(f.read())

        for root, _, files in os.walk(human_dir):
            for file in files:
                if file.endswith(".txt"):
                    with open(os.path.join(root, file), "r", encoding="utf-8") as f:
                        self.human_samples.append(f.read())
        
        print(f"Loaded {len(self.ai_samples)} AI and {len(self.human_samples)} Human samples.")

    def evaluate(self, threshold: float = 60.0):
        # Result buckets
        tp, tn, fp, fn = 0, 0, 0, 0
        total_time = 0

        print("\n--- Evaluating AI Samples ---")
        for i, text in enumerate(self.ai_samples):
            t0 = time.time()
            res = analyze_forensic(text)
            total_time += (time.time() - t0)
            
            # If confidence >= threshold, it's AI (Correct)
            if res.get("confidence", 0) >= threshold:
                tp += 1
                print(f" [OK] AI Sample {i+1}: {res['confidence']}%")
            else:
                fn += 1
                print(f" [FAIL] AI Sample {i+1}: {res['confidence']}% (FN)")
                print(f"      Signals: {res.get('signals')}")
                print(f"      Reasons: {res.get('reasons')}")

        print("\n--- Evaluating Human Samples ---")
        for i, text in enumerate(self.human_samples):
            t0 = time.time()
            res = analyze_forensic(text)
            total_time += (time.time() - t0)
            
            # If confidence < threshold, it's NOT AI (Correct)
            if res.get("confidence", 0) < threshold:
                tn += 1
                print(f" [OK] Human Sample {i+1}: {res['confidence']}%")
            else:
                fp += 1
                print(f" [FAIL] Human Sample {i+1}: {res['confidence']}% (FP)")
                print(f"      Signals: {res.get('signals')}")
                print(f"      Reasons: {res.get('reasons')}")

        # Metrics
        accuracy = (tp + tn) / (tp + tn + fp + fn) if (tp+tn+fp+fn) > 0 else 0
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0
        f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
        avg_time = total_time / (tp + tn + fp + fn) if (tp+tn+fp+fn) > 0 else 0

        print("\n" + "="*40)
        print(" FINAL BENCHMARK RESULTS ")
        print("="*40)
        print(f"Accuracy:  {accuracy:.2%}")
        print(f"Precision: {precision:.2%}")
        print(f"Recall:    {recall:.2%}")
        print(f"F1 Score:  {f1:.3f}")
        print(f"Total:     {tp+tn+fp+fn} samples")
        print(f"Avg Time:  {avg_time:.2f}s per sample")
        print("="*40 + "\n")

    def run_split_eval(self, split: float = 0.7):
        """Runs the 70% calibration / 30% testing split evaluation."""
        random.shuffle(self.ai_samples)
        random.shuffle(self.human_samples)

        ai_cal_end = int(len(self.ai_samples) * split)
        hu_cal_end = int(len(self.human_samples) * split)

        # Calibration set (use this for threshold tuning eventually)
        ai_cal = self.ai_samples[:ai_cal_end]
        hu_cal = self.human_samples[:hu_cal_end]

        # Testing set
        ai_test = self.ai_samples[ai_cal_end:]
        hu_test = self.human_samples[hu_cal_end:]

        print(f"Split: {split*100}% Calibration, {(1-split)*100}% Testing")
        print(f"Testing on {len(ai_test)} AI and {len(hu_test)} Human samples.\n")

        # Run eval on test set
        test_bench = Benchmarker(self.dataset_path)
        test_bench.ai_samples = ai_test
        test_bench.human_samples = hu_test
        test_bench.evaluate()

if __name__ == "__main__":
    bench = Benchmarker("backend/dataset")
    bench.load_dataset()
    # Run a split evaluation
    bench.run_split_eval(split=0.7)
