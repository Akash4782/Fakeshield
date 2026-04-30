
from transformers import AutoImageProcessor, SiglipImageProcessor, ViTImageProcessor
import traceback

models = [
    "prithivMLmods/AI-vs-Deepfake-vs-Real-Siglip2",
    "onnx-community/Deep-Fake-Detector-v2-Model-ONNX"
]

for m in models:
    print(f"\n--- Testing {m} ---")
    try:
        print("Trying AutoImageProcessor...")
        proc = AutoImageProcessor.from_pretrained(m)
        print(f"SUCCESS: {type(proc).__name__}")
    except Exception as e:
        print(f"FAILED AutoImageProcessor: {e}")
        
    if "Siglip2" in m or "siglip" in m.lower():
        try:
            print("Trying SiglipImageProcessor explicitly...")
            proc = SiglipImageProcessor.from_pretrained(m)
            print(f"SUCCESS: {type(proc).__name__}")
        except Exception as e:
            print(f"FAILED SiglipImageProcessor: {e}")
            
    if "Deep-Fake-Detector-v2" in m:
        try:
            print("Trying ViTImageProcessor explicitly...")
            # Often ONNX models need the original model's processor or specific mapping
            proc = ViTImageProcessor.from_pretrained(m)
            print(f"SUCCESS: {type(proc).__name__}")
        except Exception as e:
            print(f"FAILED ViTImageProcessor: {e}")
            
        try:
            print("Trying to load from the non-ONNX parent repo...")
            parent = "prithivMLmods/Deep-Fake-Detector-v2-Model"
            proc = AutoImageProcessor.from_pretrained(parent)
            print(f"SUCCESS: {type(proc).__name__} (from parent {parent})")
        except Exception as e:
             print(f"FAILED AutoImageProcessor (parent): {e}")
