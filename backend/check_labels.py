from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

tokenizer = AutoTokenizer.from_pretrained("openai-community/roberta-large-openai-detector")
model = AutoModelForSequenceClassification.from_pretrained("openai-community/roberta-large-openai-detector").eval()

text_ai = "The intersection of philosophy and technology often reveals deep-seated biases in how we perceive progress."
text_human = "I am so happy to be here today with my friends and family. It is a beautiful day!"

for t, label in [(text_ai, "AI-LIKE"), (text_human, "HUMAN-LIKE")]:
    inputs = tokenizer(t, return_tensors="pt")
    with torch.no_grad():
        logits = model(**inputs).logits
        probs = torch.softmax(logits, dim=1)[0]
    print(f"\n[{label}] {t}")
    print(f"Prob[0]: {probs[0].item():.4f}")
    print(f"Prob[1]: {probs[1].item():.4f}")
