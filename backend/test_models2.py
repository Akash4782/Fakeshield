from transformers import pipeline

print("Testing Hello-SimpleAI/chatgpt-detector-roberta-hc3-en")
try:
    pipeline("text-classification", model="Hello-SimpleAI/chatgpt-detector-roberta-hc3-en")
    print("SUCCESS Hello-SimpleAI")
except Exception as e:
    print("Error:", e)

print("Testing TrustSafeAI/RADAR-Vicuna-7B (the one user explicitly mentioned)")
try:
    pipeline("text-classification", model="TrustSafeAI/RADAR-Vicuna-7B")
    print("SUCCESS RADAR")
except Exception as e:
    print("Error:", e)

