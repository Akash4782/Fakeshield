from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

MODEL2 = "openai-community/roberta-base-openai-detector"
print(f"Downloading {MODEL2}...")
tok = AutoTokenizer.from_pretrained(MODEL2)
mdl = AutoModelForSequenceClassification.from_pretrained(MODEL2)
print("✅ Done.")

test = "Artificial intelligence has the potential to revolutionize healthcare."
inputs = tok(test, return_tensors="pt")
with torch.no_grad():
    out = mdl(**inputs)
# OpenAI detector returns [Fake, Real] or [Real, Fake]? 
# Label 0: 'Fake', Label 1: 'Real' for some OpenAI models. 
# BUT RoBERTa-base-openai usually is 0: 'Real', 1: 'Fake'?
# Let's check config.
print(f"Labels: {mdl.config.id2label}")
probs = torch.softmax(out.logits, dim=1)[0].tolist()
print(f"Probs: {probs}")
