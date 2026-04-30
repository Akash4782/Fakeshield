import torch
import torch.nn.functional as F
from PIL import Image
from transformers import AutoImageProcessor, AutoModelForImageClassification

# Load only SigLIP2 (or the model giving 0.999)
print("Loading model...")
model_id = "umm-maybe/AI-image-detector"
device = "cuda" if torch.cuda.is_available() else "cpu"

proc = AutoImageProcessor.from_pretrained(model_id)
model = AutoModelForImageClassification.from_pretrained(model_id).to(device)
model.eval()

import os
print("REAL:")
for f in os.listdir("evaluation_dataset/real"):
    path = os.path.join("evaluation_dataset/real", f)
    img = Image.open(path).convert("RGB")
    x = proc(images=img, return_tensors="pt").to(device)
    with torch.no_grad():
        out = model(**x)
        p = F.softmax(out.logits, dim=-1)[0]
    # Class 1 is usually artificial if binary
    # Let's print all logits and probs
    print(f" {f}: Probs={p.tolist()}")

print("AI:")
for f in os.listdir("evaluation_dataset/ai"):
    path = os.path.join("evaluation_dataset/ai", f)
    img = Image.open(path).convert("RGB")
    x = proc(images=img, return_tensors="pt").to(device)
    with torch.no_grad():
        out = model(**x)
        p = F.softmax(out.logits, dim=-1)[0]
    print(f" {f}: Probs={p.tolist()}")
