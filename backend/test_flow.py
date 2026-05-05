from sentence_transformers import SentenceTransformer
from scipy.spatial.distance import cosine
import numpy as np

model = SentenceTransformer('all-MiniLM-L6-v2')
sentences = ["This is a test.", "This is a test.", "This is a test."]
embeddings = model.encode(sentences)
sims = [1 - cosine(embeddings[i], embeddings[i+1]) for i in range(len(embeddings)-1)]
print(f"Sims: {sims}")
