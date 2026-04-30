"""
FakeShield — One-time setup script
Run this before starting the server.
Downloads models and converts to ONNX for CPU speed.
"""
import os, sys, time

print("\n" + "="*60)
print("  FakeShield Text Detector — First Time Setup")
print("  This runs once. Everything offline after this.")
print("="*60 + "\n")

# ── Step 1: distilgpt2 ────────────────────────────────────────
print("[1/3] Downloading distilgpt2 (~350MB)...")
from transformers import GPT2LMHeadModel, GPT2TokenizerFast
GPT2LMHeadModel.from_pretrained("distilgpt2")
GPT2TokenizerFast.from_pretrained("distilgpt2")
print("      distilgpt2 done.\n")

# ── Step 2: RoBERTa → ONNX conversion ────────────────────────
print("[2/3] Downloading RoBERTa + converting to ONNX...")
print("      This takes 3–5 minutes. Only happens once.\n")
from optimum.onnxruntime import ORTModelForSequenceClassification
from transformers import AutoTokenizer

os.makedirs("./onnx_models/roberta", exist_ok=True)

ort_model = ORTModelForSequenceClassification.from_pretrained(
    "Hello-SimpleAI/chatgpt-detector-roberta",
    export=True
)
tokenizer = AutoTokenizer.from_pretrained(
    "Hello-SimpleAI/chatgpt-detector-roberta"
)
ort_model.save_pretrained("./onnx_models/roberta")
tokenizer.save_pretrained("./onnx_models/roberta")
print("      RoBERTa ONNX saved.\n")

# ── Step 3: Verify ────────────────────────────────────────────
print("[3/3] Verifying installation...")
from optimum.onnxruntime import ORTModelForSequenceClassification as ORT
m = ORT.from_pretrained("./onnx_models/roberta")
t = AutoTokenizer.from_pretrained("./onnx_models/roberta")
inputs = t("Test sentence", return_tensors="pt")
out = m(**inputs)
print(f"      Verification passed. Output shape: {out.logits.shape}\n")

print("="*60)
print("  SETUP COMPLETE.")
print("  Models saved. Total size: ~800MB")
print("  Run: uvicorn app.main:app --port 8001 --reload")
print("="*60 + "\n")
