import os
import torch
import numpy as np
from typing import List, Dict, Any
from sentence_transformers import SentenceTransformer
import faiss

class RetrievalEngine:
    """
    Forensic Retrieval Engine v1.0 (2026 Strategy)
    Uses embedding similarity to compare input against known AI archetypes.
    "Is this similar to how AI writes?" vs "Does this look like AI?"
    """
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = SentenceTransformer(model_name).to(self.device)
        self.dimension = 384 # MiniLM-L6-v2 dimension
        self.index = faiss.IndexFlatL2(self.dimension)
        
        # Metadata for the index
        self.labels = [] # 1 for AI, 0 for Human
        
        # Bootstrap with classic AI/Human archetypes
        self._bootstrap_index()

    def _bootstrap_index(self):
        """Pre-load the index with high-confidence archetypes."""
        ai_samples = [
            "In conclusion, it is important to note that the implications are multifaceted.",
            "Moreover, the intersection of technology and society offers a unique perspective.",
            "To summarize, the key takeaway is that leveraging robust frameworks ensures success.",
            "I hope this information helps! Let me know if you have more questions.",
            "Think of it like a bridge connecting two distant islands of knowledge.",
            "Dive deep into the intricacies of this fascinating phenomenon.",
            "The potential impact of this paradigm shift cannot be overstated."
        ]
        human_samples = [
            "I was walking down the street when I saw the most bizarre thing happen.",
            "Actually, I think the problem with this study is the sample size is way too small.",
            "So, we tried to fix the bug by restarting the server, but it didn't work.",
            "The data shows a slight correlation, but it's not statistically significant at all.",
            "Hey, can you take a look at this draft? It's still a bit messy but getting there.",
            "It was a cold morning, and the coffee was the only thing keeping me awake.",
            "We demonstrated that the proposed method outperforms existing baselines by 15%."
        ]
        
        self.add_samples(ai_samples, is_ai=True)
        self.add_samples(human_samples, is_ai=False)

    def add_samples(self, texts: List[str], is_ai: bool):
        if not texts: return
        embeddings = self.model.encode(texts, convert_to_numpy=True)
        self.index.add(embeddings)
        self.labels.extend([1 if is_ai else 0] * len(texts))

    def query(self, text: str, k: int = 5) -> Dict[str, Any]:
        """Query the index for similar authorships."""
        embedding = self.model.encode([text], convert_to_numpy=True)
        distances, indices = self.index.search(embedding, k)
        
        # Calculate AI probability based on neighbor labels
        neighbor_labels = [self.labels[i] for i in indices[0]]
        # Weights neighbors by inverse distance (1/1+dist)
        weights = [1.0 / (1.0 + d) for d in distances[0]]
        
        ai_score = sum(label * w for label, w in zip(neighbor_labels, weights)) / (sum(weights) + 1e-9)
        
        return {
            "ai_probability": round(float(ai_score), 4),
            "nearest_neighbors": neighbor_labels,
            "distances": [round(float(d), 4) for d in distances[0]]
        }

_INSTANCE = None

def get_retrieval_engine():
    global _INSTANCE
    if _INSTANCE is None:
        _INSTANCE = RetrievalEngine()
    return _INSTANCE
