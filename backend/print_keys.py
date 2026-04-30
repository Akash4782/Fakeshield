import torch
from PIL import Image
import numpy as np
from transformers import AutoProcessor, AutoImageProcessor

print("🔍 Expert Diagnostic: Checking Processor Outputs")
print("-" * 50)

# 1. X-CLIP
try:
    processor = AutoProcessor.from_pretrained("microsoft/xclip-base-patch16")
    dummy_video = [np.zeros((224, 224, 3), dtype=np.uint8) for _ in range(8)]
    inputs = processor(videos=dummy_video, return_tensors="pt")
    print(f"✅ X-CLIP Keys: {list(inputs.keys())}")
except Exception as e:
    print(f"❌ X-CLIP Failed: {e}")

# 2. VideoMAE
try:
    p_mae = AutoImageProcessor.from_pretrained("MCG-NKU/videomae-base-finetuned-kinetics")
    dummy_mae = [np.zeros((224, 224, 3), dtype=np.uint8) for _ in range(16)]
    inputs_mae = p_mae(images=dummy_mae, return_tensors="pt")
    print(f"✅ VideoMAE Keys: {list(inputs_mae.keys())}")
except Exception as e:
    print(f"❌ VideoMAE Failed: {e}")
