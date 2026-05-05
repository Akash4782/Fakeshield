import numpy as np
from sentence_transformers import SentenceTransformer
from typing import Dict, Any, List
import torch

class SemanticDriftEngine:
    """
    Forensic Semantic Drift Engine v10.0
    Analyzes 'Thought Flow Trajectory' using mpnet embeddings.
    AI writing follows a geodesic (smooth) path; human reasoning has associative jumps.
    """
    def __init__(self, device: str = "cpu"):
        self.device = "cpu"
        try:
            # Upgrade to mpnet-base-v2 as per v10 requirement
            # Explicitly force CPU to avoid meta-tensor issues
            self.model = SentenceTransformer("all-mpnet-base-v2", device="cpu")
            self.enabled = True
        except Exception as e:
            print(f"[SemanticDrift] Error loading mpnet: {e}")
            self.enabled = False

    def analyze(self, text: str) -> Dict[str, Any]:
        if not self.enabled:
            return {"score": 0.5, "details": {"error": "Model not loaded"}}

        # 1. Chunking (Overlapping sliding window)
        sentences = [s.strip() for s in text.replace("\n", " ").split(".") if len(s.split()) > 3]
        if len(sentences) < 4:
            return {"score": 0.5, "details": {"warning": "Insufficient text for trajectory analysis"}}

        # Create chunks of 2 sentences each without overlap to cut inference time in half
        chunks = [" ".join(sentences[i:i+2]) for i in range(0, len(sentences), 2)]
        
        try:
            # 2. Compute Embeddings
            embeddings = self.model.encode(chunks, normalize_embeddings=True)
            global_embedding = self.model.encode([text], normalize_embeddings=True)[0]
            
            # 3. Compute Trajectory (Cosine distance between consecutive segments)
            similarities = []
            for i in range(len(embeddings)-1):
                sim = float(np.dot(embeddings[i], embeddings[i+1]))
                similarities.append(sim)
            
            # 4. Compute Topic Deviation (Distance from global topic)
            topic_similarities = [float(np.dot(emb, global_embedding)) for emb in embeddings]
            topic_deviation_score = float(np.var(topic_similarities)) * 100 # Scale it up to make it measurable
            
            # 5. NEW FORENSIC METRICS
            
            # A. Semantic Entropy (Entropy of chunk similarity distribution)
            hist, _ = np.histogram(similarities, bins=10, range=(0, 1))
            probs = hist / (sum(hist) + 1e-9)
            semantic_entropy = -sum(p * np.log2(p + 1e-9) for p in probs)
            
            # B. Drift Variance
            sim_std = float(np.std(similarities))
            sim_mean = float(np.mean(similarities))

            # Aggregates
            # High topic deviation and high entropy = human (irregularity)
            semantic_irregularity = float(np.clip( (semantic_entropy / 3.0) * 0.5 + (topic_deviation_score / 2.0) * 0.5, 0.0, 1.0 ))
            
            # Low deviation, high mean = AI
            semantic_uniformity = float(np.clip( sim_mean * 0.7 + (1.0 - (sim_std*5)) * 0.3, 0.0, 1.0 ))
            
            # Used for per-sentence weighting
            semantic_shift = float(np.clip(sim_std * 5, 0.0, 1.0))

            return {
                "semantic_irregularity": round(semantic_irregularity, 4),
                "semantic_uniformity": round(semantic_uniformity, 4),
                "semantic_shift": round(semantic_shift, 4),
                "details": {
                    "topic_deviation": round(topic_deviation_score, 4),
                    "semantic_entropy": round(semantic_entropy, 4),
                    "semantic_consistency": round(sim_mean, 3),
                    "drift_variance": round(sim_std, 4)
                }
            }

        except Exception as e:
            print(f"[SemanticDrift] Analysis error: {e}")
            return {"score": 0.5, "details": {"error": str(e)}}
