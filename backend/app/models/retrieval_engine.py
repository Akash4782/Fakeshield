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
        self.device = "cpu"
        self.model = SentenceTransformer(model_name, device="cpu")
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
            "The potential impact of this paradigm shift cannot be overstated.",
            "It is worth noting that while these results are promising, further research is needed.",
            "By understanding the underlying mechanisms, we can better appreciate the significance.",
            "This suggests that the relationship between the two variables is inherently complex.",
            "Ultimately, the goal is to create a more efficient and sustainable ecosystem.",
            "Furthermore, the advent of modern technology has accelerated this process significantly.",
            "One must consider the broader context when evaluating these specific outcomes.",
            "The synergy between artificial intelligence and human ingenuity is transformative.",
            "This highlights the importance of maintaining a balanced perspective on innovation.",
            "An interesting point to consider is how these systems evolve over time.",
            "The core essence of this transformation lies in its ability to scale globally.",
            "From a strategic standpoint, it is essential to align these objectives clearly.",
            "The intricate nature of the data suggests a deeper level of complexity.",
            "In this regard, we should focus on the underlying patterns of behavior.",
            "The transition toward a more sustainable future is a collective responsibility.",
            "Moreover, the integration of diverse perspectives fosters a more inclusive environment.",
            "This analysis underscores the critical need for robust security frameworks.",
            "By examining the results from multiple angles, we gain a comprehensive understanding.",
            "The overarching goal of this project is to enhance user engagement significantly.",
            "It is evident that the technological landscape is shifting toward automation."
        ]
        human_samples = [
            "I was walking down the street when I saw the most bizarre thing happen.",
            "Actually, I think the problem with this study is the sample size is way too small.",
            "So, we tried to fix the bug by restarting the server, but it didn't work.",
            "The data shows a slight correlation, but it's not statistically significant at all.",
            "Hey, can you take a look at this draft? It's still a bit messy but getting there.",
            "It was a cold morning, and the coffee was the only thing keeping me awake.",
            "We demonstrated that the proposed method outperforms existing baselines by 15%.",
            "I honestly couldn't believe it when I heard the news this morning.",
            "I'm not sure if this is the right approach, but let's give it a shot anyway.",
            "The party was okay, but the music was way too loud for my taste.",
            "I've been feeling a bit overwhelmed lately with all the work piled up.",
            "Wait, did you see what happened in the last episode? That was insane!",
            "I'm just going to grab a quick bite to eat before the meeting starts.",
            "To be honest, I was expecting a bit more from the new update.",
            "Look, I don't care what the manual says, this just doesn't feel right.",
            "Man, I really need to get my act together before the final deadline hits.",
            "It's just one of those days where everything that can go wrong, does.",
            "I spent three hours debugging this morning only to find a missing semicolon.",
            "The view from the top of the mountain was absolutely breathtaking, seriously.",
            "I'm thinking about taking a road trip next month, just to clear my head.",
            "Does anyone else think the new UI is actually worse than the old one?",
            "The historical context of the industrial revolution is essential for understanding modern economics.",
            "The methodology section describes the experimental setup and the data collection process in detail.",
            "According to the latest census data, the population has grown by 12% over the last decade.",
            "The primary objective of this study was to evaluate the effectiveness of the new drug candidate.",
            "Recent advances in quantum computing have opened up new possibilities for cryptography.",
            "The researchers concluded that the observed effect was statistically significant at the 0.05 level.",
            "The implementation of the new policy resulted in a significant reduction in operational costs.",
            "The data were analyzed using a variety of statistical techniques, including regression and ANOVA.",
            "The results of the simulation are consistent with the theoretical predictions of the model.",
            "The study identifies several key factors that contribute to the success of the project."
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
