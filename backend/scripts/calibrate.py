import os
import sys
import torch
import numpy as np
from scipy.optimize import minimize

# Add path so we can import backend packages
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "app")))

from services.video.video_detector import analyze_video

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def inverse_sigmoid(p):
    p = np.clip(p, 1e-15, 1 - 1e-15)
    return np.log(p / (1 - p))

def nll_loss(T, logits, labels):
    """ Negative log likelihood loss for temperature scaling """
    scaled_logits = logits / T
    probs = sigmoid(scaled_logits)
    # clip for numerical stability
    probs = np.clip(probs, 1e-15, 1 - 1e-15)
    return -np.mean(labels * np.log(probs) + (1 - labels) * np.log(1 - probs))

def main():
    real_dir = "test_data/dataset/real"
    ai_dir = "test_data/dataset/ai"
    
    if not os.path.exists(real_dir) or not os.path.exists(ai_dir):
        print("Please run downloaded_samples.py first.")
        return

    real_videos = [os.path.join(real_dir, f) for f in os.listdir(real_dir) if f.endswith(".mp4")]
    ai_videos = [os.path.join(ai_dir, f) for f in os.listdir(ai_dir) if f.endswith(".mp4")]

    print(f"Loaded {len(real_videos)} real videos and {len(ai_videos)} AI videos.")

    labels = []
    raw_scores = []
    
    print("Running inference on REAL videos...")
    for v in real_videos:
        try:
            res = analyze_video(v)
            raw_scores.append(res['fused_score'] / 100.0)  # scale to 0-1
            labels.append(0)
            print(f"REAL video {os.path.basename(v)} -> Score: {res['fused_score']}% Verdict: {res['verdict']}")
        except Exception as e:
            print(f"Failed to process {v}: {e}")

    print("\nRunning inference on AI videos...")
    for v in ai_videos:
        try:
            res = analyze_video(v)
            raw_scores.append(res['fused_score'] / 100.0)  # scale to 0-1
            labels.append(1)
            print(f"AI video {os.path.basename(v)} -> Score: {res['fused_score']}% Verdict: {res['verdict']}")
        except Exception as e:
            print(f"Failed to process {v}: {e}")

    if not labels:
        print("No videos processed successfully.")
        return

    # Convert probability back to logit for temperature scaling
    logits = np.array([inverse_sigmoid(p) for p in raw_scores])
    labels = np.array(labels)

    # Initial temperature
    init_T = 1.0
    
    # Optimize temperature
    print("\n[Calibration] Optimizing Temperature...")
    res = minimize(nll_loss, init_T, args=(logits, labels), method='L-BFGS-B', bounds=[(0.01, 10.0)])
    opt_T = res.x[0]
    
    print(f"Optimal Temperature T found: {opt_T:.4f}")
    
    # Calculate calibrated scores
    calibrated_logits = logits / opt_T
    calibrated_probs = sigmoid(calibrated_logits)
    
    print("\n---------- CALIBRATED RESULTS ----------")
    for idx in range(len(labels)):
        v_type = "REAL" if labels[idx] == 0 else "AI"
        orig = raw_scores[idx] * 100
        calib = calibrated_probs[idx] * 100
        print(f"[{v_type}] Original: {orig:05.1f}% -> Calibrated: {calib:05.1f}%")

if __name__ == "__main__":
    main()
