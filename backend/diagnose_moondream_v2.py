import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, GenerationMixin
import os

DEVICE = "cpu"
model_id = "vikhyatk/moondream2"
revision = "2024-08-26"

print(f"Loading {model_id}...")
model = AutoModelForCausalLM.from_pretrained(
    model_id, trust_remote_code=True, revision=revision
).to(DEVICE).eval()

print(f"Top-level model class: {model.__class__.__name__}")
print(f"Top-level has generate: {hasattr(model, 'generate')}")

def find_phi(m, path="model"):
    if m.__class__.__name__ == "PhiForCausalLM":
        print(f"Found {m.__class__.__name__} at {path}. Has generate: {hasattr(m, 'generate')}")
    for name, child in m.named_children():
        find_phi(child, f"{path}.{name}")

find_phi(model)
