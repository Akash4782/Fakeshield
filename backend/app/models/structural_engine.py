import spacy
import numpy as np
from typing import Dict, Any, List
import re
try:
    import textstat
except ImportError:
    pass

class StructuralEngine:
    """
    Forensic Structural Engine v10.5 (Human-First Architecture)
    Analyzes Dependency Tree Entropy, Clause Complexity, and Structural Cadence.
    AI focuses on balanced 'clean' trees (high uniformity); Human text is 'lopsided' and irregular (structural strength).
    """
    def __init__(self):
        try:
            self.nlp = spacy.load("en_core_web_sm", disable=["ner", "lemmatizer", "textcat"])
            self.enabled = True
        except Exception as e:
            print(f"[StructuralEngine] Error loading spaCy: {e}")
            self.enabled = False

    def analyze(self, text: str) -> Dict[str, Any]:
        if not self.enabled:
            return {"structural_strength": 0.5, "high_uniformity": 0.5, "structural_variation": 0.5, "details": {"error": "spaCy not loaded"}}

        doc = self.nlp(text)
        sentences = list(doc.sents)
        if len(sentences) < 2:
            return {"structural_strength": 0.5, "high_uniformity": 0.5, "structural_variation": 0.5, "details": {"warning": "Too few sentences for structural analysis"}}

        tree_depths = []
        clause_ratios = []
        branching_factors = []
        punct_counts = []
        lengths = []
        
        for sent in sentences:
            depths = self._get_token_depths(sent.root)
            tree_depths.append(max(depths) if depths else 0)
            
            sub_clauses = sum(1 for token in sent if token.dep_ in ("advcl", "relcl", "ccomp", "xcomp"))
            clause_ratios.append(sub_clauses / (len(sent) + 1e-9))
            
            branches = [len(list(token.children)) for token in sent if len(list(token.children)) > 0]
            branching_factors.append(np.mean(branches) if branches else 0)
            
            punct_counts.append(sum(1 for token in sent if token.is_punct))
            lengths.append(len(sent))

        # --- NEW HUMAN-CENTRIC METRICS ---
        
        # A. Depth Variance
        depth_var = float(np.var(tree_depths))
        depth_var_norm = float(np.clip(depth_var / 5.0, 0.0, 1.0)) # Higher is more human
        
        # B. Punctuation Randomness
        punct_cv = float(np.std(punct_counts) / (np.mean(punct_counts) + 1e-9))
        punct_cv_norm = float(np.clip(punct_cv / 1.5, 0.0, 1.0)) # Higher is more human
        
        # C. Cadence (Sentence Length Variation)
        len_cv = float(np.std(lengths) / (np.mean(lengths) + 1e-9))
        len_cv_norm = float(np.clip(len_cv / 0.8, 0.0, 1.0)) # Higher is more human
        
        # D. Readability Entropy (via textstat)
        try:
            syllable_count = textstat.syllable_count(text)
            flesch = textstat.flesch_reading_ease(text)
            readability_complexity = float(np.clip(1.0 - (flesch / 100.0), 0.0, 1.0))
        except:
            readability_complexity = 0.5

        # E. Type-Token Ratio (Lexical Diversity)
        words = [t.text.lower() for t in doc if not t.is_punct]
        if words:
            ttr = len(set(words)) / (len(words) + 1e-9)
            ttr_norm = float(np.clip(ttr / 0.8, 0.0, 1.0)) # Higher is more human/diverse
        else:
            ttr = 0.5
            ttr_norm = 0.5

        # F. POS Entropy
        pos_counts = {}
        for t in doc:
            pos_counts[t.pos_] = pos_counts.get(t.pos_, 0) + 1
        pos_total = sum(pos_counts.values())
        pos_probs = [c / pos_total for c in pos_counts.values()]
        pos_entropy = -sum(p * np.log2(p) for p in pos_probs if p > 0)
        # Normalize: AI typically has lower POS entropy (more predictable structure)
        pos_entropy_norm = float(np.clip((pos_entropy - 2.0) / 1.5, 0.0, 1.0))

        # G. Structural Entropy (Uniformity of branching)
        flat_branches = [b for b in branching_factors if b > 0]
        if flat_branches:
            hist, _ = np.histogram(flat_branches, bins=5, range=(0, 5))
            probs = hist / (sum(hist) + 1e-9)
            entropy = -sum(p * np.log2(p + 1e-9) for p in probs)
            # Normalize: AI typically has entropy < 1.0; Human > 1.5
            entropy_norm = float(np.clip((1.5 - entropy) / 1.0, 0.0, 1.0))  # Higher means strictly organized (AI)
        else:
            entropy_norm = 0.5

        # Final Aggregates
        # v16.5 weighting: focus on cadence, entropy, and diversity
        structural_strength = (depth_var_norm * 0.25) + (punct_cv_norm * 0.2) + (len_cv_norm * 0.25) + (ttr_norm * 0.2) + (pos_entropy_norm * 0.1)
        high_uniformity = (1.0 - len_cv_norm) * 0.3 + (1.0 - punct_cv_norm) * 0.2 + (entropy_norm * 0.3) + (1.0 - ttr_norm) * 0.2
        structural_variation = (depth_var_norm + len_cv_norm + ttr_norm) / 3.0
        
        # We value Entropy and Depth Var most for 2026-level detection
        return {
            "structural_strength": round(float(structural_strength), 4),
            "high_uniformity": round(float(high_uniformity), 4),
            "structural_variation": round(float(structural_variation), 4),
            "details": {
                "avg_depth": round(float(np.mean(tree_depths)), 2),
                "depth_variance": round(depth_var, 3),
                "sentence_cadence_cv": round(len_cv, 3),
                "punctuation_randomness": round(punct_cv, 3),
                "ttr": round(ttr, 3),
                "pos_entropy": round(pos_entropy, 3)
            }
        }

    def _get_token_depths(self, token, depth=0):
        depths = [depth]
        for child in token.children:
            depths.extend(self._get_token_depths(child, depth + 1))
        return depths
