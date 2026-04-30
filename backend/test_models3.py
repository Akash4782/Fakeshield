from transformers import pipeline  # type: ignore

print("Testing Hello-SimpleAI/chatgpt-detector-roberta")
try:
    pipeline("text-classification", model="Hello-SimpleAI/chatgpt-detector-roberta")
    print("SUCCESS Hello-SimpleAI")
except Exception as e:
    print("Error:", e)

print("Testing SuperAnnotate/ai-detector")
try:
    pipeline("text-classification", model="SuperAnnotate/ai-detector")
    print("SUCCESS SuperAnnotate")
except Exception as e:
    print("Error:", e)
