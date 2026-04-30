import packaging.version
original_parse = packaging.version.parse
def safe_parse(v):
    if v is None: return original_parse("2.7.1")
    return original_parse(str(v))
packaging.version.parse = safe_parse

import torch
if not hasattr(torch, "__version__") or torch.__version__ is None:
    torch.__version__ = "2.4.0+cpu"

import torch.nn.functional as F
from PIL import Image
from transformers import AutoImageProcessor, AutoModelForImageClassification

print("Loading model...")
model_id = "Organika/sdxl-detector"
device = "cuda" if torch.cuda.is_available() else "cpu"

proc = AutoImageProcessor.from_pretrained(model_id)
model = AutoModelForImageClassification.from_pretrained(model_id).to(device)
model.eval()

img = Image.open('evaluation_dataset/real/portrait.jpg').convert("RGB")
x = proc(images=img, return_tensors="pt").to(device)
with torch.no_grad():
    out = model(**x)
    p = F.softmax(out.logits, dim=-1)[0]
    
id2label = model.config.id2label
print(f"LABELS: {id2label}")
print(f"REAL PORTRAIT PROBS: {p.tolist()}")

img2 = Image.open('evaluation_dataset/ai/portrait_ai.png').convert("RGB")
x2 = proc(images=img2, return_tensors="pt").to(device)
with torch.no_grad():
    out2 = model(**x2)
    p2 = F.softmax(out2.logits, dim=-1)[0]
    
print(f"AI PORTRAIT PROBS: {p2.tolist()}")
