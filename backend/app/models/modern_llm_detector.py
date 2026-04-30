import re
import numpy as np
from typing import Dict, List

class ModernLLMDetector:
    """
    Specialized Forensic Engine for 2026-era LLMs (Gemini, Claude, GPT-4.5)
    Focuses on 'Instructional DNA' and 'Semantic Smoothness'.
    """
    
    def __init__(self):
        # Gemini/Claude specialized transition and structural patterns
        self.modern_patterns = [
            r"at its core", r"this means that", r"in other words",
            r"to put it simply", r"think of it like", r"imagine a scenario",
            r"the reality is", r"one key takeaway", r"it is worth noting",
            r"furthermore", r"consequently", r"subsequently",
            r"moreover", r"nonetheless", r"alternatively",
            # Claude Specifics
            r"I can certainly help", r"from a [\w\s]+ perspective", r"it is important to consider",
            r"one might argue", r"it is evident that", r"it's worth highlighting",
            # Gemini Specifics
            r"think of it as", r"imagine you are", r"let's explore",
            r"the following factors", r"here is a breakdown", r"it is essential to understand"
        ]
        # Patterns of list-making and bolding common in AI instructions
        self.structural_dna = [
            r"\*\*[^*]+\*\*:",  # Bolding followed by a colon (very Gemini/Claude)
            r"^\d+\.\s+\*\*[^*]+\*\*:", # Numbered list with bolded headers
            r"^\-\s+\*\*[^*]+\*\*:",   # Bullet list with bolded headers
            r"\:\s*$",               # Ending a sentence with a colon (prelude to a list)
        ]

    def detect(self, text: str) -> Dict[str, float]:
        """
        Returns a score based on Modern LLM fingerprints.
        """
        sentences = [s.strip() for s in re.split(r'[.!?]+', text) if len(s.strip()) > 5]
        if not sentences:
            return {"modern_ai_score": 0.5, "structural_dna": 0.0, "semantic_flow": 0.5}

        # 1. Structural DNA Score
        struct_hits = 0
        for pattern in self.structural_dna:
            struct_hits += len(re.findall(pattern, text, re.MULTILINE))
        
        # Normalize: High if multiple bolded lists or colons are used
        struct_score = np.clip(struct_hits / (len(sentences) / 3 + 1), 0.0, 1.0)

        # 2. Semantic Flow (Cosine Similarity approximation)
        # AI text (especially Gemini) has extremely high semantic continuity.
        # We check for word overlap between adjacent sentences.
        similarities = []
        for i in range(len(sentences) - 1):
            words1 = set(re.findall(r'\w+', sentences[i].lower()))
            words2 = set(re.findall(r'\w+', sentences[i+1].lower()))
            if not words1 or not words2: continue
            
            intersection = words1.intersection(words2)
            # Jaccard similarity as a proxy for semantic smoothness
            score = len(intersection) / len(words1.union(words2))
            similarities.append(score)
        
        avg_flow = np.mean(similarities) if similarities else 0.0
        # AI typically stays in the 0.15 - 0.35 Jaccard range (smooth). 
        # Human writing is either very low (jumpy) or very high (repetitive).
        flow_score = 0.8 if 0.15 < avg_flow < 0.40 else 0.4

        # 3. Pattern Match Score
        pattern_hits = 0
        for p in self.modern_patterns:
            if re.search(r"\b" + p + r"\b", text, re.I):
                pattern_hits += 1
        
        lexical_score = np.clip(pattern_hits / (len(sentences) / 4 + 1), 0.0, 1.0)

        # 4. Progressive Complexity (Gemini/Claude signature)
        sent_lengths = [len(s.split()) for s in sentences]
        progression = 0.0
        if len(sent_lengths) > 3:
            first_half = np.mean(sent_lengths[:len(sent_lengths)//2])
            second_half = np.mean(sent_lengths[len(sent_lengths)//2:])
            if second_half > first_half * 1.2:
                progression = 0.6
        
        # 5. Burstiness Analysis (Coefficient of Variation)
        # AI text is 'smooth' (low CV), Humans are 'bursty' (high CV).
        burstiness_score = 0.0
        if len(sent_lengths) > 2:
            std = np.std(sent_lengths)
            mean = np.mean(sent_lengths)
            cv = std / mean if mean > 0 else 0
            # AI typically has CV < 0.3. Human writing often has CV > 0.5.
            if cv < 0.25:
                burstiness_score = 0.8  # Very AI-like smoothness
            elif cv < 0.40:
                burstiness_score = 0.5
        
        # Combined Modern LLM Score (v17.3 Optimized)
        # Weights: Struct (25%), Flow (15%), Lexical (20%), Progression (15%), Burstiness (25%)
        final_score = (struct_score * 0.25 + flow_score * 0.15 + lexical_score * 0.20 + 
                       progression * 0.15 + burstiness_score * 0.25)
        
        return {
            "modern_ai_score": round(float(final_score), 4),
            "structural_dna": round(float(struct_score), 4),
            "semantic_flow": round(float(avg_flow), 4),
            "progressive_complexity": round(float(progression), 4),
            "rhythm_smoothness": round(float(burstiness_score), 4)
        }
