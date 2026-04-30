import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

MODEL = "openai-community/roberta-base-openai-detector"
tokenizer = AutoTokenizer.from_pretrained(MODEL)
model = AutoModelForSequenceClassification.from_pretrained(MODEL)

print(f"Config labels: {model.config.id2label}")

text_human = "I went to the store to buy some milk."
text_ai = "The simulation of human intelligence processes by machines is called artificial intelligence."

def get_prob(text):
    inputs = tokenizer(text, return_tensors="pt")
    with torch.no_grad():
        logits = model(**inputs).logits
    return torch.softmax(logits, dim=1)

print(f"Human text: {get_prob(text_human)}")
print(f"AI text: {get_prob(text_ai)}")
