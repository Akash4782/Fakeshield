from optimum.onnxruntime import ORTModelForImageClassification
from transformers import AutoImageProcessor
import torch

hf_id = "onnx-community/Deep-Fake-Detector-v2-Model-ONNX"

print(f"Testing ONNX load for {hf_id}...")
try:
    # This is expected to FAIL with "Too many ONNX model files"
    model = ORTModelForImageClassification.from_pretrained(
        hf_id, provider="CPUExecutionProvider"
    )
    print("SUCCESS (Unexpectedly)")
except Exception as e:
    print(f"EXPECTED FAIL: {e}")

print("\nTesting FIXED ONNX load...")
try:
    # Specify the file name
    model = ORTModelForImageClassification.from_pretrained(
        hf_id, provider="CPUExecutionProvider", file_name="model.onnx"
    )
    print("SUCCESS (FIXED)")
    
    # Test a dummy inference to check for Segfault
    processor = AutoImageProcessor.from_pretrained(hf_id)
    from PIL import Image
    img = Image.new('RGB', (224, 224), color = (73, 109, 137))
    inputs = processor(images=img, return_tensors="pt")
    outputs = model(**inputs)
    print(f"Output Logits: {outputs.logits}")
    
except Exception as e:
    print(f"FAIL (FIXED VERSION): {e}")
    import traceback
    traceback.print_exc()
