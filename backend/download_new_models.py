from transformers import pipeline

print("[1/2] Downloading coai detector v2 (GPT-4 academic text)...")
pipeline("text-classification", model="coai/roberta-ai-detector-v2")

print("[2/2] Downloading Hello-SimpleAI v2 (updated dataset)...")
pipeline("text-classification", model="Hello-SimpleAI/chatgpt-detector-roberta-hc3-en")

print("Done.")
