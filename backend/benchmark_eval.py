# benchmark_eval.py — EVALUATION SUITE
"""
Runs the full FakeShield Video Forensic Lab on real and AI samples.
Generates an accuracy report and forensic signal breakdown.
"""
import os
import json
import time
import sys

# Ensure backend directory is in path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from app.services.video.video_detector import analyze_video

EVAL_DIR = "backend/eval_samples"
REPORT_FILE = "backend/benchmark_report.json"

def run_benchmark():
    if not os.path.exists(EVAL_DIR):
        print(f"❌ Error: {EVAL_DIR} not found. Run downloads first.")
        return

    samples = [f for f in os.listdir(EVAL_DIR) if f.endswith(".mp4")]
    if not samples:
        print(f"❌ No samples found in {EVAL_DIR}.")
        return

    print(f"🎬 Starting Benchmark on {len(samples)} samples...")
    print("-" * 60)

    results = []
    
    for filename in samples:
        video_path = os.path.join(EVAL_DIR, filename)
        is_ai_ground_truth = filename.startswith("sora")
        
        print(f"🔍 Analyzing: {filename} (GT: {'AI' if is_ai_ground_truth else 'REAL'})")
        
        start_time = time.time()
        try:
            # Run analysis
            report = analyze_video(video_path, max_frames=32)
            elapsed = time.time() - start_time
            
            verdict = report.get("verdict", "UNKNOWN")
            fused_score = report.get("fused_score", 0.0)
            
            # Simple accuracy check
            is_correct = False
            if is_ai_ground_truth and verdict in ["AI_GENERATED", "LIKELY_AI"]:
                is_correct = True
            elif not is_ai_ground_truth and verdict in ["LIKELY_REAL", "UNCERTAIN"]:
                # Uncertain is better than false positive for real samples
                is_correct = True
                
            res = {
                "filename": filename,
                "ground_truth": "AI" if is_ai_ground_truth else "REAL",
                "verdict": verdict,
                "score": fused_score,
                "is_correct": is_correct,
                "elapsed_sec": round(elapsed, 2),
                "signal_scores": report.get("signal_scores", {}),
                "robustness": report.get("robustness", {}),
                "provenance": report.get("provenance", {})
            }
            results.append(res)
            
            status_icon = "✅" if is_correct else "❌"
            print(f"   {status_icon} Verdict: {verdict} ({fused_score}%) | Time: {elapsed:.1f}s")
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
            results.append({
                "filename": filename,
                "error": str(e)
            })

    # Summary
    total = len([r for r in results if "error" not in r])
    correct = len([r for r in results if r.get("is_correct")])
    accuracy = (correct / total * 100) if total > 0 else 0

    print("-" * 60)
    print(f"📊 BENCHMARK COMPLETE")
    print(f"✅ Accuracy: {accuracy:.1f}% ({correct}/{total})")
    
    # Save report
    summary = {
        "timestamp": time.ctime(),
        "total_samples": total,
        "correct": correct,
        "accuracy_pct": accuracy,
        "results": results
    }
    
    with open(REPORT_FILE, "w") as f:
        json.dump(summary, f, indent=4)
        
    print(f"📝 Report saved to {REPORT_FILE}")

if __name__ == "__main__":
    run_benchmark()
