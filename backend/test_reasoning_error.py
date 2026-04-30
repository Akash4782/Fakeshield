import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, GenerationMixin, GenerationConfig
from PIL import Image
import os

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

print(f"Testing Moondream2 on {DEVICE}...")
model_id = "vikhyatk/moondream2"
revision = "2024-08-26"
model = AutoModelForCausalLM.from_pretrained(
    model_id, trust_remote_code=True, revision=revision
).to(DEVICE).eval()

# FIX: Explicitly initialize generation config
try:
    model.generation_config = GenerationConfig.from_model_config(model.config)
    print("GenerationConfig initialized successfully.")
except Exception as e:
    print(f"GenerationConfig Initialization Failed: {e}")

def patch_recursive(m, path="model"):
    if m.__class__.__name__ == "PhiForCausalLM" or (
        not hasattr(m, "generate") and hasattr(m, "prepare_inputs_for_generation")
    ):
        if not isinstance(m, GenerationMixin):
            print(f"Patching {path} ({m.__class__.__name__}) with GenerationMixin...")
            m.__class__ = type(
                m.__class__.__name__, 
                (m.__class__, GenerationMixin), 
                {}
            )
    
    for name, child in m.named_children():
        patch_recursive(child, f"{path}.{name}")

patch_recursive(model)
tokenizer = AutoTokenizer.from_pretrained(model_id, revision=revision)

# Test detection
print(f"Generation Config: {model.generation_config}")

try:
    # Create a dummy image
    img = Image.new('RGB', (224, 224), color = (73, 109, 137))
    enc_image = model.encode_image(img)
    answer = model.answer_question(enc_image, "What color is this image?", tokenizer)
    print(f"Answer: {answer}")
except Exception as e:
    import traceback
    traceback.print_exc()
