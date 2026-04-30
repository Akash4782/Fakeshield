print("ST1: Importing torch")
import torch
print("ST2: Importing transformers")
try:
    from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
    print("ST3: Transformers imported")
except Exception as e:
    print(f"ST3: Transformers import failed: {e}")

print("ST4: Importing other stuff")
import numpy as np
import time, os

print("ST5: Success")
