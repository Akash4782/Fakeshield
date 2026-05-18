import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

m_id = "Hello-SimpleAI/chatgpt-detector-roberta"
tok = AutoTokenizer.from_pretrained(m_id)
mdl = AutoModelForSequenceClassification.from_pretrained(m_id).eval()

text = "Deep learning is a branch of Artificial Intelligence and Machine Learning where computers learn patterns directly from large amounts of data using structures called **neural networks**. The idea is inspired by the human brain, where neurons connect and pass signals to each other. In deep learning, artificial neurons are arranged in multiple layers, and because these networks contain many layers, the method is called \"deep\" learning. Instead of manually telling the computer every rule, the system learns rules automatically from examples. For instance, if you want a machine to recognize cats in images, traditional programming would require writing explicit rules like \"cats have ears, whiskers, tails,\" which quickly becomes impossible for complex problems. Deep learning avoids this by feeding thousands or millions of cat images into a neural network so it can learn those features itself. A deep learning model is built using an architecture called an **Artificial Neural Network (ANN)**. The network contains three main parts: the input layer, hidden layers, and output layer. The input layer receives raw"

import re
sentences = re.split(r'(?<=[.!?])\s+', text)

inputs = tok(sentences, return_tensors="pt", max_length=128, truncation=True, padding=True)
with torch.no_grad():
    probs = torch.softmax(mdl(**inputs).logits, dim=1)[:, 1].tolist()

for s, p in zip(sentences, probs):
    print(f"P={p:.4f} | {s}")

print("MEAN:", sum(probs)/len(probs))
