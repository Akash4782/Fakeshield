import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

m_id = "openai-community/roberta-large-openai-detector"
tokenizer = AutoTokenizer.from_pretrained(m_id)
model = AutoModelForSequenceClassification.from_pretrained(m_id).eval()

human_text = "I went to the store today and bought some apples. It was a nice day."
ai_text = "The implementation of neural networks in modern data analytics underscores the importance of scalable infrastructure."

for text, label in [(human_text, "HUMAN"), (ai_text, "AI")]:
    inputs = tokenizer(text, return_tensors="pt")
    with torch.no_grad():
        logits = model(**inputs).logits
        probs = torch.softmax(logits, dim=1)[0]
        print(f"[{label}] Probs: {probs.tolist()}")
