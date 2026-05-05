from transformers import AutoConfig
config = AutoConfig.from_pretrained("openai-community/roberta-large-openai-detector")
print(f"Labels: {config.id2label}")
