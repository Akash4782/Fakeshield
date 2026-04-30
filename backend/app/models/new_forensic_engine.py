"""
FakeShield — Forensic Engine v16 (Elite Fusion)
============================================================
v16 UPGRADE: Implements the research-backed "Perfect Detector" architecture.
- Adaptive Fusion of DeBERTa-v3, Binoculars, and DivEye signals.
- Optimized for CPU performance using distilled models.
- Enhanced "Uncertainty Resolver" using LLM Reasoning Judge.

Pipeline:
  1. Multi-Vector Ensemble (Neural + Statistical + Zero-Shot)
  2. Structural Complexity Audit (spaCy)
  3. Semantic Drift Analysis (MPNet)
  4. LLM Judge Reasoning (Selective Fallback)
"""

# Heavy imports moved inside functions for lazy loading
import re
import time
import torch
import numpy as np
from typing import Dict, Any, List

# Engines are lazy-initialized
_STRUCTURAL_ENGINE     = None
_SEMANTIC_DRIFT_ENGINE = None

def get_structural_engine():
    global _STRUCTURAL_ENGINE
    if _STRUCTURAL_ENGINE is None:
        from app.models.structural_engine import StructuralEngine
        _STRUCTURAL_ENGINE = StructuralEngine()
    return _STRUCTURAL_ENGINE

def get_semantic_drift_engine():
    global _SEMANTIC_DRIFT_ENGINE
    if _SEMANTIC_DRIFT_ENGINE is None:
        from app.models.semantic_drift import SemanticDriftEngine
        _SEMANTIC_DRIFT_ENGINE = SemanticDriftEngine()
    return _SEMANTIC_DRIFT_ENGINE

def get_device():
    return "cuda" if torch.cuda.is_available() else "cpu"

_PPL_TOK  = None
_PPL_MDL  = None
_BINO     = None
_JUDGE    = None


def load_models():
    global _PPL_TOK, _PPL_MDL, _BINO, _JUDGE
    import time
    from transformers import GPT2LMHeadModel, GPT2Tokenizer
    from app.models.loader_sync import MODEL_LOAD_LOCK
    from app.models.binoculars import Binoculars
    from app.models.forensic_judge import ForensicJudge
    from app.models.text_classifier_ensemble import (
        load_neural_detector,
        load_ppl_engine,
        set_binoculars,
    )

    t_total = time.time()
    
    print("\n" + "="*50)
    print("--- [Engine v16] Initializing Forensic Suite ---")
    print("="*50)

    # 1. Neural Detector
    print(f"[1/4] Loading Neural Transformer (ONNX Optimized)...", flush=True)
    t1 = time.time()
    try:
        load_neural_detector()
        print(f"      OK ({time.time()-t1:.2f}s)", flush=True)
    except Exception as e:
        print(f"      FAILED: {e}", flush=True)

    # 2. Statistical Engine
    print(f"[2/4] Loading Statistical PPL Engine (DistilGPT2)...", flush=True)
    t2 = time.time()
    try:
        if _PPL_TOK is None:
            _PPL_TOK = GPT2Tokenizer.from_pretrained("distilgpt2", use_fast=True)
            _PPL_TOK.pad_token = _PPL_TOK.eos_token
            with MODEL_LOAD_LOCK:
                _PPL_MDL = GPT2LMHeadModel.from_pretrained("distilgpt2").to(get_device()).eval()
        load_ppl_engine(_PPL_TOK, _PPL_MDL)
        print(f"      OK ({time.time()-t2:.2f}s)", flush=True)
    except Exception as e:
        print(f"      FAILED: {e}", flush=True)

    # 3. Binoculars Engine
    print(f"[3/4] Loading Binoculars Zero-Shot Engine (Pythia-70M)...", flush=True)
    t3 = time.time()
    try:
        if _BINO is None:
            _BINO = Binoculars(device=get_device())
        set_binoculars(_BINO)
        print(f"      OK ({time.time()-t3:.2f}s)", flush=True)
    except Exception as e:
        print(f"      FAILED: {e}", flush=True)

    # 4. LLM Judge
    print(f"[4/4] Connecting Forensic Judge (Gemini API)...", flush=True)
    t4 = time.time()
    try:
        if _JUDGE is None:
            _JUDGE = ForensicJudge()
        print(f"      OK ({time.time()-t4:.2f}s)", flush=True)
    except Exception as e:
        print(f"      FAILED: {e}", flush=True)

    print("="*50)
    print(f"--- [Engine v16] SYSTEM READY ({time.time()-t_total:.2f}s) ---")
    print("="*50 + "\n")


def _verdict(prob: float):
    if prob >= 0.70:   return "AI GENERATED",  "CRITICAL"
    elif 0.40 <= prob <= 0.60: return "UNCERTAIN", "MEDIUM"
    elif prob < 0.30:  return "AUTHENTIC",     "SAFE"
    else:              return "UNCERTAIN",     "LOW"


def analyze_forensic(text: str, mode: str = "deep") -> Dict[str, Any]:
    global _BINO
    from app.models.text_classifier_ensemble import (
        ensemble_predict,
        ensemble_predict_sentences,
    )
    from app.models.structural_engine import StructuralEngine
    from app.models.semantic_drift import SemanticDriftEngine

    if _BINO is None: load_models()

    t0 = time.time()
    clean_text = text.strip()
    words = clean_text.split()
    n_words = len(words)

    if n_words < 120:
        return {
            "error": "REJECTED (SHORT)",
            "verdict": "REJECTED",
            "threat_level": "NONE",
            "score": 0.5,
            "forensic_reasoning": f"Sample size insufficient ({n_words} words). 2026-level forensic reliability requires >120 words for stable signal fusion."
        }

    # ── Step 1: Parallel Ensemble Analysis ──
    import concurrent.futures
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        future_ensemble = executor.submit(ensemble_predict, clean_text)
        
        def safe_struct():
            try: return get_structural_engine().analyze(clean_text)
            except: return {"structural_strength": 0.5, "high_uniformity": 0.5, "details": {}}
                
        def safe_drift():
            try: return get_semantic_drift_engine().analyze(clean_text)
            except: return {"semantic_irregularity": 0.5, "semantic_uniformity": 0.5, "details": {}}

        future_struct = executor.submit(safe_struct)
        future_drift = executor.submit(safe_drift)

        ensemble = future_ensemble.result()
        struct_res = future_struct.result()
        drift_res = future_drift.result()

    ai_prob  = ensemble["ai_probability"]
    layers   = ensemble["layer_scores"]
    raw      = ensemble["raw_metrics"]

    # Cache reuse for highlights
    internal = ensemble.get("_neural_internal", {})
    cached_sentences     = internal.get("sentences", [])
    cached_neural_scores = internal.get("sentence_scores", [])

    # ── Signal Aggregation ──
    signals = {
        "classifier_signal": ensemble["layer_scores"]["neural_classifier"],
        "ppl_signal": ensemble["layer_scores"]["ppl_score"],
        "binoculars_signal": ensemble["layer_scores"]["binoculars_score"],
        "lexical_signal": ensemble["layer_scores"]["lexical_score"],
        "modern_fingerprint": ensemble["layer_scores"].get("modern_fingerprint", 0),
        "surprisal_variance": ensemble["layer_scores"].get("surprisal_var", 0),
        "structural_strength": ensemble["layer_scores"]["stylometry_score"],
        "human_shield": ensemble["signals"].get("human_shield", 0)
    }

    verdict, threat = _verdict(ai_prob)
    confidence = "HIGH" if ai_prob < 0.35 or ai_prob > 0.70 else "MEDIUM"

    # ── Step 2: LLM Judge for Ambiguous or High-Disagreement Cases ──
    judge_reasoning    = ""
    foreign_indicators = []
    
    # Uncertainty Gate: Trigger judge for 0.4 - 0.6 or high disagreement
    signal_disagreement = abs(layers["neural_classifier"] - layers["binoculars_score"])
    
    if mode == "deep" and (0.40 <= ai_prob <= 0.60 or signal_disagreement > 0.30):
        try:
            if _JUDGE:
                res = _JUDGE.evaluate(clean_text, layers)
                j_score = res.get("ai_probability", 0.5)
                judge_reasoning    = res.get("reasoning", "")
                foreign_indicators = res.get("suspicious_indicators", [])
                
                # Weighted Fusion with Judge
                j_weight = 0.50 # Balanced weight for reasoning
                ai_prob = ai_prob * (1.0 - j_weight) + j_score * j_weight
                verdict, threat = _verdict(ai_prob)
        except Exception as e:
            print(f"[Engine] Judge failure: {e}")

    # ── Step 3: Sentence Highlights ──
    clean_text_flat = clean_text.replace("\n", " ")
    raw_sentences = [s.strip() for s in re.split(r'(?<=[.!?])\s+', clean_text_flat) if s.strip()]
    valid_ids     = [i for i, s in enumerate(raw_sentences) if len(s.split()) >= 5]
    valid_sents   = [raw_sentences[i] for i in valid_ids]

    if cached_sentences == valid_sents and cached_neural_scores:
        sent_ai_scores = ensemble_predict_sentences(
            valid_sents,
            cached_neural_scores=cached_neural_scores,
            doc_context=layers,
        )
    else:
        sent_ai_scores = ensemble_predict_sentences(valid_sents, doc_context=layers)

    valid_highlight_data = dict(zip(valid_ids, sent_ai_scores))
    highlights = []
    for i, s in enumerate(raw_sentences):
        if i not in valid_highlight_data:
            highlights.append({"sentence": s, "ai_score": None, "perplexity": 0, "label": "too_short"})
            continue
        data = valid_highlight_data[i]
        sp = data["ai_score"]
        ppl = data["perplexity"]
        label = "AI" if sp >= 0.55 else ("UNCERTAIN" if sp >= 0.38 else "HUMAN")
        highlights.append({
            "sentence": s, 
            "ai_score": round(sp * 100, 1), 
            "perplexity": ppl,
            "label": label
        })

    # ── Final Response Mapping ──
    return {
        "verdict":         verdict,
        "threat_level":    threat,
        "score":           round(ai_prob, 4),
        "confidence":      confidence,
        "confidence_level": confidence,
        "agreement_score": round(1.0 - abs(layers["neural_classifier"] - layers["binoculars_score"]), 3),
        "stability_score": round(struct_res.get("high_uniformity", 0.5), 3),

        "signals": {
            "classifier_signal":    layers.get("neural_classifier", 0.5),
            "ppl_signal":           layers.get("ppl_score", 0.5),
            "burstiness_signal":    layers.get("burstiness_score", 0.5),
            "binoculars_signal":    layers.get("binoculars_score", 0.5),
            "lexical_signal":       layers.get("lexical_score", 0.0),
            "surprisal_variance":   layers.get("surprisal_var", 0.0),
            "structural_strength":  struct_res.get("structural_strength", 0.5),
            "semantic_irregularity": drift_res.get("semantic_irregularity", 0.5),
        },

        "linguistic_profile": {
            "syntactic_complexity": "HIGH" if struct_res.get("structural_strength", 0.5) > 0.6 else "LOW",
            "entropy_bits_per_char": round(raw.get("perplexity", 0) / 100, 3),
            "burstiness_raw":        raw.get("burstiness", 0),
        },

        "forensic_reasoning": judge_reasoning or _explain_v16(verdict, layers, raw),
        "indicators":         foreign_indicators or _get_indicators(layers, raw),
        "structural_details": struct_res.get("details", {}),
        "semantic_details":   drift_res.get("details", {}),
        "sentence_highlights": highlights,

        "word_count":     len(clean_text.split()),
        "processing_time": f"{round(time.time() - t0, 2)}s",
        "engine_version": "16.0.0-ELITE",
    }


def _explain_v16(verdict: str, layers: dict, raw: dict) -> str:
    neu  = layers.get("neural_classifier", 0.5)
    bino = layers.get("binoculars_score", 0.5)
    ppl  = raw.get("perplexity", 50.0)
    svar = layers.get("surprisal_var", 0.0)
    
    parts = []
    if neu > 0.70: parts.append("Advanced DeBERTa-v3 transformer identifies deep synthetic patterns.")
    if bino > 0.70: parts.append("Zero-shot cross-perplexity audit (Binoculars) confirms machine origin.")
    if ppl < 20: parts.append(f"Extremely low perplexity ({ppl:.1f}) indicates high token predictability.")
    if svar < 1.0: parts.append("Low surprisal variance suggests mechanical, non-rhythmic writing style.")
    
    if not parts:
        if "HUMAN" in verdict: parts.append("Linguistic variability and high entropy align with natural human authorship.")
        else: parts.append("Ensemble signals indicate a probable synthetic origin across multiple vectors.")
    
    return " ".join(parts)

def _get_indicators(layers: dict, raw: dict) -> List[str]:
    ind = []
    if layers.get("lexical_score", 0) > 0.6: ind.append("High AI Vocabulary Density")
    if layers.get("surprisal_var", 0) < 0.8: ind.append("Low Rhythmic Variance (DivEye)")
    if raw.get("perplexity", 0) < 15: ind.append("Highly Predictable Token Stream")
    if layers.get("neural_classifier", 0) > 0.9: ind.append("Transformer Fingerprint Detected")
    return ind
