import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

m_id = "openai-community/roberta-large-openai-detector"
tok = AutoTokenizer.from_pretrained(m_id)
mdl = AutoModelForSequenceClassification.from_pretrained(m_id).eval()

ai_text = "Furthermore, it is important to note that artificial intelligence underscores the importance of data ethics."
inputs = tok(ai_text, return_tensors="pt")
with torch.no_grad():
    logits = mdl(**inputs).logits
    probs = torch.softmax(logits, dim=1)[0]
    print(f"Text: {ai_text}")
    print(f"Prob[0] (AI?): {probs[0].item():.4f}")
    print(f"Prob[1] (Human?): {probs[1].item():.4f}")

human_text = "I went to the store today and bought some apples for my grandmother's pie."
inputs = tok(human_text, return_tensors="pt")
with torch.no_grad():
    logits = mdl(**inputs).logits
    probs = torch.softmax(logits, dim=1)[0]
    print(f"\nText: {human_text}")
    print(f"Prob[0] (AI?): {probs[0].item():.4f}")
    print(f"Prob[1] (Human?): {probs[1].item():.4f}")
