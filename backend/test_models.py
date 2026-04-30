from transformers import pipeline

print("Testing andrewMacmurray/roberta-large-ai-vs-human-text-detector")
try:
    pipeline("text-classification", model="andrewMacmurray/roberta-large-ai-vs-human-text-detector")
except Exception as e:
    print("Error:", e)

print("Testing Hello-SimpleAI/chatgpt-detector-roberta-hc3-en")
try:
    pipeline("text-classification", model="Hello-SimpleAI/chatgpt-detector-roberta-hc3-en")
except Exception as e:
    print("Error:", e)
