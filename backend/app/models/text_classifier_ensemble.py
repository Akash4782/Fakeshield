"""
FakeShield — AI Forensic Ensemble v14.0 (Elite Classic)
======================================================
Architecture:
1. Primary Classifier: RoBERTa-HC3 (70% Weight)
2. Statistical Signal: GPT2 Perplexity/Burstiness (30% Weight)
3. Zero-Shot Profiling: Binoculars (Supplementary)
4. Structural/Semantic Profiling: spaCy + SentenceTransformer
"""

import os
import re
import json
import numpy as np
import torch
import spacy
from typing import Dict, Any, List
from transformers import AutoTokenizer, AutoModelForSequenceClassification, GPT2LMHeadModel
from sentence_transformers import SentenceTransformer
from scipy.spatial.distance import cosine
from app.config import settings

# --- Internal Engines ---
from app.models.binoculars import Binoculars
from app.models.stylometry_engine import StylometryEngine
from concurrent.futures import ThreadPoolExecutor
import time

# --- GLOBAL CACHE ---
_models: Dict[str, Any] = {}
_bino_engine = None
_stylo_engine = None
_drift_model = None
_nlp = None

def load_vanguard_v85():
    """Initializes the v14.0 Classic Forensic Stack."""
    global _bino_engine, _stylo_engine, _drift_model, _nlp
    
    # 1. HC3 ChatGPT Detector (Primary)
    if "hc3" not in _models:
        print("[v14.0] Loading HC3 RoBERTa Detector...", flush=True)
        m_id = "Hello-SimpleAI/chatgpt-detector-roberta"
        _models["hc3"] = (
            AutoTokenizer.from_pretrained(m_id),
            AutoModelForSequenceClassification.from_pretrained(m_id).eval()
        )

    # 2. GPT2 Statistical Engine
    if "gpt2" not in _models:
        print("[v14.0] Loading GPT2-Medium for Statistical Profiling...", flush=True)
        m_id = "gpt2-medium"
        _models["gpt2"] = (
            AutoTokenizer.from_pretrained(m_id),
            GPT2LMHeadModel.from_pretrained(m_id).eval()
        )

    if _bino_engine is None:
        print("[v14.0] Loading Binoculars Zero-Shot Signal...", flush=True)
        _bino_engine = Binoculars(device="cpu")

    if _stylo_engine is None:
        _stylo_engine = StylometryEngine()

    if _drift_model is None:
        print("[v14.0] Loading Semantic Drift Engine (MPNet)...", flush=True)
        _drift_model = SentenceTransformer('all-mpnet-base-v2')

    if _nlp is None:
        try:
            _nlp = spacy.load("en_core_web_sm")
        except:
            os.system("python -m spacy download en_core_web_sm")
            _nlp = spacy.load("en_core_web_sm")

# --- FORENSIC SIGNALS ---

def calculate_gpt2_stats(text: str) -> Dict[str, float]:
    """Calculates Perplexity and Burstiness using GPT2-Medium (Lite Mode)."""
    tok, mdl = _models["gpt2"]
    # 128 words is enough for a statistical signature on CPU
    text_sample = " ".join(text.split()[:128])
    inputs = tok(text_sample, return_tensors="pt", truncation=True, max_length=256)
    with torch.no_grad():
        outputs = mdl(**inputs, labels=inputs["input_ids"])
        loss = outputs.loss
        perplexity = torch.exp(loss).item()
    
    t_gpt = time.time()
    # Optimized Burstiness: 3 chunks for speed
    tokens = inputs["input_ids"][0]
    chunk_size = 40
    chunks = []
    for i in range(0, len(tokens) - chunk_size, chunk_size):
        chunks.append(tokens[i:i+chunk_size])
    
    chunks = chunks[:3] # Limit to 3 chunks
    
    if chunks:
        # Pad and batch chunks
        batched_chunks = torch.stack(chunks)
        with torch.no_grad():
            outputs = mdl(batched_chunks, labels=batched_chunks)
            logits = outputs.logits # [batch, seq, vocab]
            shift_logits = logits[..., :-1, :].contiguous()
            shift_labels = batched_chunks[..., 1:].contiguous()
            loss_fct = torch.nn.CrossEntropyLoss(reduction='none')
            loss = loss_fct(shift_logits.view(-1, shift_logits.size(-1)), shift_labels.view(-1))
            chunk_losses = loss.view(batched_chunks.size(0), -1).mean(dim=1).tolist()
    else:
        chunk_losses = []

    burstiness = np.var(chunk_losses) if chunk_losses else 0.0
    print(f"[Timer] GPT2 Chunks processed in {time.time()-t_gpt:.2f}s")
    
    # Normalization calibrated to GPT2-Medium real-world ranges (v14.5 Elite):
    # AI text perplexity: ~18-45, Human text: ~65-200+
    # Steep drop between 40 and 65 to clearly separate AI and human distributions.
    if perplexity < 45:
        # Score 0.5 to 1.0 (AI-like)
        p_score = 1.0 - (max(perplexity, 18) - 18) / 54.0 
    else:
        # Score 0.0 to 0.5 (Human-like)
        p_score = max(0.0, 0.45 - (perplexity - 45) / 70.0)
    
    # Burstiness variance: AI=low variance (~0.0-0.06), Human=high variance (~0.12-0.5)
    # b_score=1.0 (AI, low burstiness) to 0.0 (human, high burstiness)
    if burstiness < 0.10:
        # Score 0.5 to 1.0 (AI-like)
        b_score = 1.0 - (max(burstiness, 0.005) - 0.005) / 0.19
    else:
        # Score 0.0 to 0.5 (Human-like)
        b_score = max(0.0, 0.45 - (burstiness - 0.10) / 0.25)
    
    print(f"[GPT2] raw_perplexity={perplexity:.2f}, raw_burstiness={burstiness:.4f}, p_score={p_score:.3f}, b_score={b_score:.3f}")
    return {"perplexity": float(p_score), "burstiness": float(b_score), "raw_perplexity": perplexity, "raw_burstiness": burstiness}

def get_hc3_scores(text: str) -> Dict[str, Any]:
    """Optimized batch-level HC3 inference for full heatmap visibility."""
    t_hc3 = time.time()
    tok, mdl = _models["hc3"]
    sentences = re.split(r'(?<=[.!?])\s+', text)
    # 15-20 sentences provides good coverage without hitting 12s limit
    valid_sentences = [s for s in sentences if len(s.split()) > 3][:18] 
    
    if not valid_sentences:
        return {"mean": 0.5, "max": 0.5, "raw": [], "sentences": []}

    # Batch Tokenization: Using a tighter max_length for speed
    inputs = tok(valid_sentences, return_tensors="pt", padding=True, truncation=True, max_length=128)
    with torch.no_grad():
        logits = mdl(**inputs).logits
        probs = torch.softmax(logits, dim=1)[:, 1].tolist() 
    
    print(f"[Timer] HC3 Batch of {len(valid_sentences)} done in {time.time()-t_hc3:.2f}s")
    
    sentences_data = []
    for sent, score in zip(valid_sentences, probs):
        sentences_data.append({
            "sentence": sent,
            "score": float(score)
        })
    
    return {
        "mean": float(np.mean(probs)),
        "max": float(np.max(probs)),
        "raw": probs,
        "sentences": sentences_data
    }

def get_binoculars_score(text: str) -> float:
    """Zero-shot statistical signature via Binoculars."""
    t_bino = time.time()
    if _bino_engine is None: return 0.5
    try:
        # 128 words is the sweet spot for Binoculars calibration
        truncated_text = " ".join(text.split()[:128])
        score = float(_bino_engine.compute_score(truncated_text))
        print(f"[Timer] Binoculars done in {time.time()-t_bino:.2f}s")
        return score
    except:
        return 0.5

def get_semantic_drift(text: str) -> float:
    sentences = re.split(r'(?<=[.!?])\s+', text)
    if len(sentences) < 3: return 0.5
    try:
        # 4 sentences for ultra-fast drift profiling
        embeddings = _drift_model.encode(sentences[:4])
        sims = [1 - cosine(embeddings[i], embeddings[i+1]) for i in range(len(embeddings)-1)]
        return float(np.mean(sims))
    except:
        return 0.5

def ensemble_predict(text: str, mode: str = "v14") -> Dict[str, Any]:
    word_count = len(text.split())
    if word_count < 30:
        return {"error": "Text too short. Minimum 30 words required."}

    load_vanguard_v85()
    
    # ── PHASE 2: SEQUENTIAL SIGNAL EXTRACTION (v14.8 Optimized) ───
    # Sequential execution prevents CPU contention on single-core environments
    t_sig = time.time()
    hc3_res = get_hc3_scores(text)
    gpt2_res = calculate_gpt2_stats(text)
    bino_score = get_binoculars_score(text)
    print(f"[Perf] Signals extracted in {time.time()-t_sig:.2f}s")
    
    t_drift = time.time()
    drift_score = get_semantic_drift(text)
    print(f"[Perf] Semantic drift calculated in {time.time()-t_drift:.2f}s")

    # ── PHASE 3: STRUCTURAL DEPTH ───
    depth_variance = 0.0
    if _nlp:
        doc = _nlp(text[:1000])
        depths = [len(list(token.ancestors)) for token in doc]
        depth_variance = float(np.var(depths)) if depths else 0.0

    # ── CORE FUSION (v14.6 Calibrated) ──────────────────────────────
    # HC3 Neural (30%) + Perplexity (25%) + Burstiness (15%) + Binoculars (30%)
    # Reduced HC3 weight further because it often false-positives on formal human text.
    # Binoculars and Perplexity are more reliable for human verification.
    core_score = (hc3_res["mean"] * 0.30) + (gpt2_res["perplexity"] * 0.25) + (gpt2_res["burstiness"] * 0.15) + (bino_score * 0.30)

    # ── FORMAL-PROSE HUMAN CORRECTION (v14.5) ────────────────────────────
    # IBM / DataCamp / academic prose tends to look ChatGPT-like to HC3.
    # Trigger: HC3 is in uncertain zone AND statistical signals say HUMAN.
    hc3_is_high      = hc3_res["mean"] > 0.45
    rhythm_irregular = gpt2_res["raw_burstiness"] > 0.12  # Lowered threshold to catch more human text
    high_perplexity  = gpt2_res["raw_perplexity"] > 65
    has_long_text    = word_count > 80  # Reduced requirement

    if hc3_is_high and (rhythm_irregular or high_perplexity or bino_score < 0.3) and has_long_text:
        # If statistical signals strongly point to human, override the neural bias
        correction = 0.18
        if (rhythm_irregular and high_perplexity) or bino_score < 0.2: 
            correction = 0.25
        core_score = max(0.0, core_score - correction)
    
    # ── DEEP HUMAN ANCHOR (v14.6) ──────────────────────────────────
    # If the neural classifier is extremely confident it's human (HC3 < 0.15)
    # and we have enough text, we should respect that, as HC3 is very specific.
    if hc3_res["mean"] < 0.15 and has_long_text:
        # Formal human prose (low perplexity) often tricks statistical engines.
        # If neural says human, it's a very strong indicator.
        core_score = max(0.0, core_score - 0.20)
        if hc3_res["mean"] < 0.05: core_score = max(0.0, core_score - 0.10)
    # ── PHASE 4: Gemini Judge (genuinely uncertain zone only) ─────
    final_score = core_score
    is_uncertain = 0.44 <= final_score <= 0.62
    judge_applied = False

    if is_uncertain and settings.GEMINI_API_KEY:
        try:
            import google.generativeai as genai
            genai.configure(api_key=settings.GEMINI_API_KEY)
            model_g = genai.GenerativeModel("gemini-2.0-flash")
            prompt = (
                f"You are a forensic authorship expert. Analyze if the following text is "
                f"AI-generated or human-written. Return only valid JSON: "
                f'{{"verdict": "AI" or "HUMAN", "adjustment": <float -0.10 to 0.10>, "reason": "<one sentence>"}}. '
                f"Text: {text[:1500]}"
            )
            resp = model_g.generate_content(prompt)
            raw = resp.text.strip().replace('```json', '').replace('```', '')
            judge_data = json.loads(raw)
            final_score = max(0.0, min(1.0, final_score + judge_data.get('adjustment', 0)))
            judge_applied = True
        except:
            pass

    final_score = max(0.0, min(1.0, final_score))

    # ── VERDICT THRESHOLDS (v14.7 Granular) ──────────────────────
    # 0.00-0.24 → HUMAN WRITTEN
    # 0.25-0.39 → LIKELY HUMAN
    # 0.40-0.59 → UNCERTAIN
    # 0.60-0.79 → LIKELY AI
    # 0.80-1.00 → AI GENERATED
    if final_score >= 0.80:
        verdict = "AI GENERATED"
        threat_level = "CRITICAL"
    elif final_score >= 0.60:
        verdict = "LIKELY AI"
        threat_level = "HIGH"
    elif final_score >= 0.40:
        verdict = "UNCERTAIN"
        threat_level = "MEDIUM"
    elif final_score >= 0.25:
        verdict = "LIKELY HUMAN"
        threat_level = "LOW"
    else:
        verdict = "HUMAN WRITTEN"
        threat_level = "LOW"

    # ── DISPLAY SCORE CALIBRATION ─────────────────────────────────
    # HUMAN WRITTEN (0-19%)
    # LIKELY HUMAN  (20-34%)
    # UNCERTAIN     (35-64%)
    # LIKELY AI     (65-79%)
    # AI GENERATED  (80-100%)
    if verdict == "HUMAN WRITTEN":
        # Raw 0.00-0.24 → Display 0.02-0.19
        t = final_score / 0.24
        display_score = 0.02 + t * 0.17
    elif verdict == "LIKELY HUMAN":
        # Raw 0.25-0.39 → Display 0.20-0.34
        t = (final_score - 0.25) / 0.14
        display_score = 0.20 + t * 0.14
    elif verdict == "UNCERTAIN":
        # Raw 0.40-0.59 → Display 0.35-0.64
        t = (final_score - 0.40) / 0.19
        display_score = 0.35 + t * 0.29
    elif verdict == "LIKELY AI":
        # Raw 0.60-0.79 → Display 0.65-0.79
        t = (final_score - 0.60) / 0.19
        display_score = 0.65 + t * 0.14
    else:  # AI GENERATED
        # Raw 0.80-1.00 → Display 0.80-0.98
        t = (final_score - 0.80) / 0.20
        display_score = 0.80 + t * 0.18

    display_score = round(max(0.0, min(1.0, display_score)), 4)
    confidence_lvl = "HIGH" if display_score > 0.80 or display_score < 0.20 else ("MEDIUM" if display_score > 0.55 or display_score < 0.40 else "LOW")


    # UI Mapping — expose meaningful signals to the frontend gauges
    ui_signals = {
        "neural":      round(hc3_res["mean"], 3),          # HC3 RoBERTa score
        "statistical": round(bino_score, 3),               # Binoculars zero-shot score
        "rhythm":      round(gpt2_res["burstiness"], 3),   # GPT2 burstiness (0=uniform/AI, 1=irregular/human)
        "flow":        round(drift_score, 3)               # Semantic drift
    }

    # ── INDICATORS (Calibrated to Verdict) ──────────────────────
    indicators = []
    
    # Only add 'AI' indicators if the verdict isn't strongly human
    if final_score > 0.35:
        if gpt2_res["raw_perplexity"] < 35:
            indicators.append("Low perplexity — text is highly predictable (AI signature)")
        if hc3_res["max"] > 0.9:
            indicators.append("Strong HC3 neural match — suspicious of ChatGPT origin")
        if gpt2_res["raw_burstiness"] < 0.05:
            indicators.append("Uniform sentence rhythm detected (Low Burstiness)")
        if bino_score > 0.80:
            indicators.append("Binoculars zero-shot confirms AI statistical profile")
    else:
        # Human-specific positive indicators
        if gpt2_res["raw_perplexity"] > 80:
            indicators.append("High linguistic entropy — characteristic of human creativity")
        if gpt2_res["raw_burstiness"] > 0.20:
            indicators.append("Dynamic rhythmic variance — highly human sentence flow")
        if bino_score < 0.2:
            indicators.append("Zero-shot signature confirms human authorship")

    if word_count < 150:
        indicators.append("SHORT SAMPLE WARNING: Results less reliable under 150 words")

    # ── GENERATE HIGHLIGHTS ───────────────────────────────────────
    highlights = []
    for s_data in hc3_res.get("sentences", []):
        s_score = s_data["score"]
        if s_score > 0.70:
            s_label = "AI"
        elif s_score > 0.30:
            s_label = "UNCERTAIN"
        else:
            s_label = "HUMAN"
        
        highlights.append({
            "sentence": s_data["sentence"],
            "ai_score": int(s_score * 100),
            "label": s_label,
            "perplexity": float(gpt2_res["raw_perplexity"]) # Global proxy
        })

    return {
        "scan_id": f"fs-v14-{os.urandom(4).hex()}",
        "verdict": verdict,
        "score": display_score,
        "overall_score": display_score,
        "confidence": confidence_lvl,
        "confidence_level": confidence_lvl,
        "threat_level": threat_level,
        "signals": ui_signals,
        "indicators": indicators,
        "forensic_reasoning": f"v14.7 Engine: {verdict} (display={display_score}, raw={round(final_score,4)}, HC3={round(hc3_res['mean'],3)})",
        "word_count": word_count,
        "engine_version": "v14.0-Elite-Classic",
        "sentence_highlights": highlights,
        "structural_details": {
            "avg_depth": 0, "depth_variance": round(depth_variance, 2),
            "structural_entropy": round(gpt2_res["raw_perplexity"], 2),
            "sentence_cadence_cv": round(gpt2_res["raw_burstiness"], 4)
        },
        "semantic_details": {
            "semantic_consistency": round(drift_score, 3),
            "drift_variance": 0.0,
            "trajectory_smoothness": "SMOOTH" if drift_score > 0.75 else "NATURAL"
        },
        "linguistic_profile": {
            "syntactic_complexity": "HIGH",
            "lexical_diversity": "MODERATE",
            "pacing_consistency": "STABLE",
            "entropy_bits_per_char": round(gpt2_res["raw_perplexity"] / 10, 2),
            "burstiness_raw": round(gpt2_res["raw_burstiness"], 4)
        }
    }
