import torch
print(f"Direct torch version: {torch.__version__}")
try:
    from transformers.utils import import_utils
    print(f"Transformers torch version: {import_utils._torch_version}")
except Exception as e:
    import traceback
    traceback.print_exc()
