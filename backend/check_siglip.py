from transformers import AutoImageProcessor
model_id = "Ateeqq/ai-vs-human-image-detector"
try:
    proc = AutoImageProcessor.from_pretrained(model_id)
    print(f"Processor: {proc}")
    print(f"Mean: {proc.image_mean if hasattr(proc, 'image_mean') else 'N/A'}")
    print(f"Std: {proc.image_std if hasattr(proc, 'image_std') else 'N/A'}")
except Exception as e:
    print(f"Error: {e}")
