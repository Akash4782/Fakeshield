
import torch
from transformers import AutoModelForAudioClassification, AutoFeatureExtractor
import os

def test_load(model_id):
    print(f"Testing load for {model_id}")
    try:
        model = AutoModelForAudioClassification.from_pretrained(
            model_id,
            low_cpu_mem_usage=False,
            device_map=None
        )
        print(f"  Model loaded. Device: {next(model.parameters()).device}")
        
        # Check for meta tensors
        has_meta = any(p.device.type == 'meta' for p in model.parameters())
        print(f"  Has meta tensors: {has_meta}")
        
        if has_meta:
            print("  FOUND META TENSORS! This is the issue.")
        
        model.to("cpu")
        print("  Successfully moved to CPU")
    except Exception as e:
        print(f"  FAILED: {e}")

if __name__ == "__main__":
    test_load("MattyB95/AST-ASVspoof5-Synthetic-Voice-Detection")
    test_load("abhishtagatya/wavlm-base-960h-itw-deepfake")
