"""
Download desklib/ai-text-detector-v1.01
#1 model on RAID 2024 Benchmark (DeBERTa-v3-large)
"""
from transformers import AutoTokenizer, AutoModel, AutoConfig

MODEL_ID = "desklib/ai-text-detector-v1.01"

print(f"Downloading tokenizer for {MODEL_ID}...")
tok = AutoTokenizer.from_pretrained(MODEL_ID)
print("Tokenizer OK.")

print(f"Downloading config for {MODEL_ID}...")
cfg = AutoConfig.from_pretrained(MODEL_ID)
print("Config OK.")

print(f"Downloading model weights for {MODEL_ID}...")
mdl = AutoModel.from_pretrained(MODEL_ID)
print("Model OK.")

print(f"\n✅ {MODEL_ID} downloaded successfully and cached.")
print(f"   Model type: {cfg.model_type}")
print(f"   Hidden size: {cfg.hidden_size}")
