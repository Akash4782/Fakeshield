import shutil, os
from pathlib import Path

print("Clearing gpt2-medium cache...")

cache_dir = Path.home() / ".cache" / "huggingface" / "hub"
deleted   = []

if cache_dir.exists():
    for item in cache_dir.iterdir():
        name = item.name.lower()
        if "gpt2" in name and "medium" in name:
            print(f"  Deleting: {item.name}")
            shutil.rmtree(item) if item.is_dir() else item.unlink()
            deleted.append(item.name)

if not deleted:
    print("  No gpt2-medium cache found.")
    print("  Checking alternate locations...")
    if cache_dir.exists():
        for item in cache_dir.iterdir():
            if "gpt2" in item.name.lower():
                print(f"  Found: {item.name}")

print("\nRe-downloading gpt2-medium...")
from transformers import GPT2LMHeadModel, GPT2TokenizerFast

model = GPT2LMHeadModel.from_pretrained(
    "gpt2-medium",
    force_download=True   # bypass cache
)
tok   = GPT2TokenizerFast.from_pretrained(
    "gpt2-medium",
    force_download=True
)

# Verify immediately
import torch, torch.nn.functional as F, math

params = sum(p.numel() for p in model.parameters())
print(f"\nParameter count: {params:,}")
print(f"Expected:        354,823,168")

if params < 300_000_000:
    print("WRONG MODEL — still not gpt2-medium")
else:
    print("gpt2-medium verified ✓")

# Quick inference test
model.eval()
tok.pad_token = tok.eos_token
test_text = (
    "Furthermore, machine learning represents a significant "
    "advancement in artificial intelligence. In conclusion, "
    "these systems are widely used across various industries. "
    "The algorithms identify patterns and make predictions "
    "based on large amounts of training data."
)
enc = tok(test_text, return_tensors="pt",
          truncation=True, max_length=128)
with torch.no_grad():
    out  = model(**enc, labels=enc["input_ids"])
    loss = out.loss.item()
    logits = out.logits
    log_p  = F.log_softmax(logits, dim=-1)
    ids    = enc["input_ids"][0]
    tok_lp = log_p[0, range(len(ids)-1), ids[1:]]
    mean_lp = tok_lp.mean().item()

ppl = math.exp(min(loss, 20))
print(f"\nTest on AI text:")
print(f"  PPL:     {round(ppl, 2)}")
print(f"  mean_lp: {round(mean_lp, 4)}")
print()
if mean_lp < -7.0:
    print("STILL BROKEN — mean_lp too extreme")
    print("Your gpt2-medium download is corrupted.")
    print("Try: pip install --upgrade transformers torch")
elif 1.5 <= abs(mean_lp) <= 4.0:
    print("gpt2-medium working correctly ✓")
    print(f"Expected score on this text: ~{round((1/(1+math.exp((ppl-65)/28)))*100)}%")
else:
    print(f"Unusual value: {round(mean_lp,3)} — may still be wrong model")
