from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

m_id = "Hello-SimpleAI/chatgpt-detector-roberta"
tokenizer = AutoTokenizer.from_pretrained(m_id)
model = AutoModelForSequenceClassification.from_pretrained(m_id).eval()

text_human = "The rapid development of machine learning has brought significant changes to various industries. Researchers are continuously exploring new architectures to improve efficiency."
text_ai = "As an AI language model, I can tell you that artificial intelligence is a rapidly growing field with many exciting applications in everyday life."

inputs_human = tokenizer([text_human], return_tensors="pt")
inputs_ai = tokenizer([text_ai], return_tensors="pt")

with torch.no_grad():
    out_human = torch.softmax(model(**inputs_human).logits, dim=1)
    out_ai = torch.softmax(model(**inputs_ai).logits, dim=1)

print("Human text probabilities (Class 0, Class 1):", out_human.tolist())
print("AI text probabilities (Class 0, Class 1):", out_ai.tolist())
