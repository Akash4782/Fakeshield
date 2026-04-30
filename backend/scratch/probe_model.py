import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

model_name = "vraj33/ai-text-detector-deberta"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

print(f"Model: {model_name}")
print(f"Config id2label: {model.config.id2label}")

texts = ["This is a human written sentence.", "The artificial intelligence system generated this response."]
for text in texts:
    inputs = tokenizer(text, return_tensors="pt")
    outputs = model(**inputs)
    probs = torch.softmax(outputs.logits, dim=-1)
    print(f"Text: {text}")
    print(f"Probs: {probs}")
