import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
import os

DEVICE = "cpu"
model_id = "vikhyatk/moondream2"
revision = "2024-08-26"

print(f"Loading {model_id}...")
try:
    model = AutoModelForCausalLM.from_pretrained(
        model_id, trust_remote_code=True, revision=revision
    ).to(DEVICE).eval()
    tokenizer = AutoTokenizer.from_pretrained(model_id, revision=revision)

    # ── TEST THE PATCH ──
    from transformers import GenerationMixin
    def patch_gen(model_obj):
        if not hasattr(model_obj, "generate") or not isinstance(model_obj, GenerationMixin):
            print(f"Patching {model_obj.__class__.__name__}...")
            model_obj.__class__ = type(
                model_obj.__class__.__name__, 
                (model_obj.__class__, GenerationMixin), 
                {}
            )

    patch_gen(model)
    if hasattr(model, 'phi'):
        patch_gen(model.phi)

    print(f"phi has generate after patch: {hasattr(model.phi, 'generate')}")

    # Test 'answer_question' (which calls phi.generate)
    print("Testing answer_question...")
    from PIL import Image
    import requests
    # Create dummy white image
    dummy_img = Image.new('RGB', (224, 224), color='white')
    
    # This should NO LONGER fail with 'PhiForCausalLM' object has no attribute 'generate'
    enc_image = model.encode_image(dummy_img)
    answer = model.answer_question(enc_image, "What is in the image?", tokenizer)
    print(f"Answer: {answer}")

except Exception as e:
    import traceback
    traceback.print_exc()
    print(f"Error: {e}")
