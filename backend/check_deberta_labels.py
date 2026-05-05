from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

def check_labels():
    m_id = "OU-Advacheck/deberta-v3-base-daigenc-mgt1a"
    tokenizer = AutoTokenizer.from_pretrained(m_id)
    model = AutoModelForSequenceClassification.from_pretrained(m_id)
    
    print(f"Config: {model.config.id2label}")
    
    texts = [
        "The quick brown fox jumps over the lazy dog.", # Human
        "In the current era of technological advancement, it is essential to recognize the transformative impact of artificial intelligence." # AI-ish
    ]
    
    for text in texts:
        inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
        with torch.no_grad():
            logits = model(**inputs).logits
            probs = torch.softmax(logits, dim=1)[0]
            print(f"\nText: {text}")
            print(f"Probabilities: {probs.tolist()}")

if __name__ == "__main__":
    check_labels()
