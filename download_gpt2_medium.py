# download_gpt2_medium.py
from transformers import GPT2LMHeadModel, GPT2TokenizerFast
import time

print("="*50)
print("Downloading gpt2-medium (~1.4GB)")
print("This runs ONCE. Cached forever after.")
print("="*50 + "\n")

t = time.time()

print("[1/2] Downloading tokenizer...")
GPT2TokenizerFast.from_pretrained("gpt2-medium")
print("      Tokenizer done.\n")

print("[2/2] Downloading model weights...")
GPT2LMHeadModel.from_pretrained("gpt2-medium")
print("      Model done.\n")

elapsed = round(time.time() - t, 1)
print("="*50)
print(f"DONE in {elapsed}s")
print("gpt2-medium cached at ~/.cache/huggingface/")
print("Run your server now.")
print("="*50)
