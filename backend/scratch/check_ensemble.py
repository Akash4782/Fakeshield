import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

def check_model(model_name, label_human_idx, label_ai_idx):
    print(f"\n--- Model: {model_name} ---")
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name)
    print(f"Config labels: {model.config.id2label}")
    
    texts = {
        "Human (Self-written)": "I am writing this sentence myself to test the system. I really hope it works correctly because I spent a lot of time on it.",
        "AI (ChatGPT)": "The Industrial Revolution, which began in the late 18th century, was a period of significant technological and socio-economic change that transformed agrarian societies into industrialized urban ones."
    }
    
    for label, text in texts.items():
        inputs = tokenizer(text, return_tensors="pt")
        with torch.no_grad():
            logits = model(**inputs).logits
        probs = torch.softmax(logits, dim=1)[0]
        print(f"{label}: P(AI)={probs[label_ai_idx].item():.4f}, P(Human)={probs[label_human_idx].item():.4f}")

# Current config in new_forensic_engine.py:
# CLF1: Hello-SimpleAI/chatgpt-detector-roberta (0: Human, 1: AI)
# CLF2: openai-community/roberta-base-openai-detector (0: Fake/AI, 1: Real/Human)
# CLF3: desklib/ai-text-detector-v1.01 (0: Human, 1: AI)

print("Verifying Ensemble Labels...")
check_model("Hello-SimpleAI/chatgpt-detector-roberta", 0, 1)
check_model("openai-community/roberta-base-openai-detector", 1, 0)
check_model("desklib/ai-text-detector-v1.01", 0, 1)
