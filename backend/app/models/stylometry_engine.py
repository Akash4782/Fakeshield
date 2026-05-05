import spacy
import numpy as np
from collections import Counter
import math

class StylometryEngine:
    """
    Advanced Stylometric Analysis Engine (2026 Standard)
    Uses spaCy for deep linguistic feature extraction.
    """
    def __init__(self):
        try:
            self.nlp = spacy.load("en_core_web_sm", disable=["ner", "lemmatizer"])
            print("[Stylometry] Engine initialized with en_core_web_sm.")
        except Exception as e:
            print(f"[Stylometry] Failed to load spaCy model: {e}")
            self.nlp = None

    def analyze(self, text: str) -> dict:
        if not self.nlp:
            return {"stylometry_score": 0.5, "signals": {}}

        doc = self.nlp(text)
        sentences = list(doc.sents)
        if not sentences:
            return {"stylometry_score": 0.5, "signals": {}}

        # 1. POS Entropy (Measure of syntactic variety)
        pos_counts = Counter([token.pos_ for token in doc])
        total_pos = sum(pos_counts.values())
        pos_entropy = -sum((count/total_pos) * math.log2(count/total_pos) for count in pos_counts.values())
        
        # 2. Dependency Depth (Measure of structural complexity)
        # Higher depth often indicates human nuance
        def get_depth(token):
            if not list(token.children):
                return 1
            return 1 + max(get_depth(child) for child in token.children)
        
        depths = [get_depth(sent.root) for sent in sentences]
        avg_depth = np.mean(depths)
        depth_var = np.std(depths)

        # 3. Burstiness (Advanced)
        sent_lengths = [len(sent) for sent in sentences]
        burstiness = np.std(sent_lengths) / (np.mean(sent_lengths) + 1e-9)

        # 4. Lexical Density (Content words / Total words)
        content_pos = {"NOUN", "VERB", "ADJ", "ADV"}
        content_words = sum(1 for token in doc if token.pos_ in content_pos)
        lexical_density = content_words / (len(doc) + 1e-9)

        # SCORING LOGIC (Research-grounded 2026)
        # AI characteristics: Low POS Entropy (< 2.8), Low Depth Var (< 1.5), Low Burstiness (< 0.3)
        ai_pos_sig = 1.0 - np.clip((pos_entropy - 2.2) / 1.0, 0, 1)
        ai_burst_sig = 1.0 - np.clip((burstiness - 0.2) / 0.6, 0, 1)
        ai_depth_sig = 1.0 - np.clip((avg_depth - 3.0) / 4.0, 0, 1)
        
        # Combine signals
        stylometry_score = (ai_pos_sig * 0.4) + (ai_burst_sig * 0.4) + (ai_depth_sig * 0.2)

        return {
            "stylometry_score": float(np.clip(stylometry_score, 0, 1)),
            "pos_entropy": float(pos_entropy),
            "avg_depth": float(avg_depth),
            "burstiness": float(burstiness),
            "lexical_density": float(lexical_density),
            "signals": {
                "repetitive_syntax": ai_pos_sig > 0.7,
                "monotonous_rhythm": ai_burst_sig > 0.7,
                "shallow_structure": ai_depth_sig > 0.7
            }
        }
