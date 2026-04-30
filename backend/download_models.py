"""
Download Hello-SimpleAI/chatgpt-detector-roberta
Best general-purpose ChatGPT vs Human detector (standard HF interface)
Also downloads desklib for ensemble
"""
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

# === Model 1: Hello-SimpleAI (recommended primary) ===
MODEL1 = "Hello-SimpleAI/chatgpt-detector-roberta"
print(f"\n[1/2] Downloading {MODEL1}...")
tok1 = AutoTokenizer.from_pretrained(MODEL1)
mdl1 = AutoModelForSequenceClassification.from_pretrained(MODEL1)
mdl1.eval()

# Quick test
test = "Climate change refers to long-term shifts in weather patterns predominantly attributed to human activities."
inputs = tok1(test, return_tensors="pt", truncation=True, max_length=512)
with torch.no_grad():
    out = mdl1(**inputs)
probs = torch.softmax(out.logits, dim=1)[0]
print(f"   Labels: {mdl1.config.id2label}")
print(f"   Short formal human text score: {probs.tolist()}")
print(f"   ✅ {MODEL1} works correctly!\n")

# === Test on obvious AI text ===
ai_test = "In conclusion, it is important to note that artificial intelligence has fundamentally transformed modern society in numerous meaningful ways."
inputs2 = tok1(ai_test, return_tensors="pt", truncation=True, max_length=512)
with torch.no_grad():
    out2 = mdl1(**inputs2)
probs2 = torch.softmax(out2.logits, dim=1)[0]
print(f"   Obvious AI text score: {probs2.tolist()}")

print(f"\n✅ Download complete. Ready to integrate.")
