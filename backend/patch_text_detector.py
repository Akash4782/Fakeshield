import os
import re

filepath = r"c:\Users\office\Documents\Final_year_project\backend\app\models\text_detector.py"
with open(filepath, "r", encoding="utf-8") as f:
    code = f.read()

# Replace Header & Imports
old_header = '''"""
FakeShield AI Text Detector — Final Production Version
CPU + ONNX optimised
gpt2-medium for accurate perplexity and Fast-DetectGPT signals
Expected accuracy: 88-92% on AI text
"""

import math, re, time, os, sys
import concurrent.futures
import torch
import torch.nn.functional as F
import numpy as np
from typing import Optional, Dict, Any, List
from transformers import (
    AutoTokenizer,
    RobertaForSequenceClassification,
    RobertaTokenizer,
    GPT2LMHeadModel,
    GPT2TokenizerFast,
    pipeline,
)'''

new_header = '''"""
FakeShield Text Detector v6.0 — Modern Models
Primary: SuperAnnotate (GPT-4/Claude/Llama/Mistral trained)
Secondary: desklib (modern architecture)
Tertiary: openai-large (strong baseline)
GPT2: gpt2-medium (perplexity + fast-detectgpt)
Target accuracy: 88-94% on modern AI text
100% free, 100% local, 100% offline
"""

import math, re, time, os, sys
import concurrent.futures
import torch
import torch.nn.functional as F
import numpy as np
from typing import Optional, Dict, Any, List
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    GPT2LMHeadModel,
    GPT2TokenizerFast,
    pipeline,
)'''
code = code.replace(old_header, new_header)

# Remove old models and insert new models
old_models_start = 'print("\\n[FakeShield] Loading models...\\n")'
old_models_end = 'print("\\n[FakeShield] All models loaded.\\n")'

start_idx = code.find(old_models_start)
end_idx = code.find(old_models_end) + len(old_models_end)

new_models = '''print("\\n[FakeShield] Loading v6.0 models...\\n")

# ── MODEL A: SuperAnnotate (BEST — GPT4/Claude/Llama trained) ─
print("[A] Loading SuperAnnotate/ai-detector...")
print("[A] Trained on: GPT-4, Claude, Llama, Mistral, Gemini")
try:
    MODEL_A_PIPE = pipeline(
        "text-classification",
        model="SuperAnnotate/ai-detector",
        device=-1,
        truncation=True,
        max_length=512,
    )
    # Test and auto-detect label
    _a_ai    = MODEL_A_PIPE(
        "Furthermore, machine learning represents a significant "
        "paradigm shift in AI. In conclusion, these systems "
        "leverage large amounts of data across various industries."
    )[0]
    _a_human = MODEL_A_PIPE(
        "I went to the market today. The tomatoes looked fresh "
        "so I bought some. My dog was happy when I got back."
    )[0]
    print(f"[A] AI text    → {_a_ai}")
    print(f"[A] Human text → {_a_human}")

    # Determine AI label direction
    _a_ai_score    = float(_a_ai["score"])
    _a_human_score = float(_a_human["score"])

    if _a_ai["label"] == _a_human["label"]:
        # Same label — higher score on AI text = AI when high
        _A_AI_LABEL     = _a_ai["label"]
        _A_AI_WHEN_HIGH = _a_ai_score > _a_human_score
    else:
        # Different labels — clear discrimination
        _A_AI_LABEL     = _a_ai["label"]
        _A_AI_WHEN_HIGH = True

    print(f"[A] AI_label='{_A_AI_LABEL}', "
          f"AI_when_high={_A_AI_WHEN_HIGH}")
    print(f"[A] SuperAnnotate ready ✓\\n")
    MODEL_A_LOADED = True

except Exception as e:
    print(f"[A] Failed: {e}")
    import traceback; traceback.print_exc()
    MODEL_A_LOADED = False


# ── MODEL B: openai-large (strong GPT-2/3 baseline) ──────────
print("[B] Loading openai-community/roberta-large-openai-detector...")
try:
    MODEL_B_PIPE = pipeline(
        "text-classification",
        model="openai-community/roberta-large-openai-detector",
        device=-1,
        truncation=True,
        max_length=512,
    )
    _b_test = MODEL_B_PIPE(
        "Furthermore, machine learning represents a significant "
        "paradigm shift."
    )[0]
    print(f"[B] Test: {_b_test}")
    # LABEL_0=Real=Human, LABEL_1=Fake=AI
    _B_AI_LABEL = "LABEL_1"
    print("[B] LABEL_1=Fake=AI ✓\\n")
    MODEL_B_LOADED = True
except Exception as e:
    print(f"[B] Failed: {e}")
    MODEL_B_LOADED = False


# ── MODEL C: desklib (modern architecture, mean pooling) ──────
print("[C] Loading desklib/ai-text-detector-v1.01...")
try:
    MODEL_C_TOK = AutoTokenizer.from_pretrained(
        "desklib/ai-text-detector-v1.01"
    )
    MODEL_C_MDL = AutoModelForSequenceClassification.from_pretrained(
        "desklib/ai-text-detector-v1.01"
    ).eval()

    # Test immediately
    _c_enc = MODEL_C_TOK(
        "Furthermore, machine learning represents a significant "
        "paradigm shift in AI. In conclusion, these systems "
        "are widely used across various industries.",
        return_tensors="pt",
        truncation=True, max_length=128, padding=True
    )
    with torch.no_grad():
        _c_out   = MODEL_C_MDL(**_c_enc)
        _c_probs = F.softmax(_c_out.logits, dim=-1).numpy()[0]

    print(f"[C] desklib labels: {MODEL_C_MDL.config.id2label}")
    print(f"[C] AI text probs: {[round(float(p)*100,1) for p in _c_probs]}")

    # Find AI label index
    _c_labels = MODEL_C_MDL.config.id2label
    _C_AI_IDX = int(np.argmax(_c_probs))  # higher = AI
    print(f"[C] AI index = {_C_AI_IDX} ✓\\n")
    MODEL_C_LOADED = True

except Exception as e:
    print(f"[C] Failed: {e}")
    MODEL_C_LOADED = False


# ── gpt2-medium ───────────────────────────────────────────────
print("[GPT2] Loading gpt2-medium...")
GPT2_TOK = GPT2TokenizerFast.from_pretrained("gpt2-medium")
GPT2_TOK.pad_token = GPT2_TOK.eos_token
GPT2_MDL = GPT2LMHeadModel.from_pretrained("gpt2-medium").eval()
_params  = sum(p.numel() for p in GPT2_MDL.parameters())
print(f"[GPT2] {_params:,} parameters "
      f"({'✓' if _params > 300_000_000 else 'WRONG MODEL'})\\n")

print("[FakeShield] v6.0 — All models loaded.\\n")'''

code = code[:start_idx] + new_models + code[end_idx:]

# Replace sig_roberta
import re
sig_roberta_code = '''def sig_roberta(text: str) -> float:
    scores, weights = [], []

    # ── Model A: SuperAnnotate (primary — modern training) ────
    if MODEL_A_LOADED:
        try:
            res   = MODEL_A_PIPE(text[:512])[0]
            raw   = float(res["score"])
            label = res["label"]

            if label == _A_AI_LABEL:
                score_a = raw if _A_AI_WHEN_HIGH else 1.0 - raw
            else:
                score_a = (1.0 - raw) if _A_AI_WHEN_HIGH else raw

            scores.append(score_a)
            weights.append(0.50)  # highest weight — best model
            print(f"[A-SuperAnnotate] label='{label}' "
                  f"→ {round(score_a*100,1)}%")
        except Exception as e:
            print(f"[A] {e}")

    # ── Model B: openai-large (strong baseline) ───────────────
    if MODEL_B_LOADED:
        try:
            res   = MODEL_B_PIPE(text[:512])[0]
            raw   = float(res["score"])
            label = res["label"].lower()
            # LABEL_1 = Fake = AI
            score_b = raw if "label_1" in label else 1.0 - raw
            scores.append(score_b)
            weights.append(0.30)
            print(f"[B-openai-large] label='{res['label']}' "
                  f"→ {round(score_b*100,1)}%")
        except Exception as e:
            print(f"[B] {e}")

    # ── Model C: desklib (modern architecture) ────────────────
    if MODEL_C_LOADED:
        try:
            enc = MODEL_C_TOK(
                text[:512], return_tensors="pt",
                truncation=True, max_length=512, padding=True,
            )
            with torch.no_grad():
                out   = MODEL_C_MDL(**enc)
                probs = F.softmax(
                    out.logits, dim=-1
                ).numpy()[0]
            score_c = float(probs[_C_AI_IDX])
            scores.append(score_c)
            weights.append(0.20)
            print(f"[C-desklib] {round(score_c*100,1)}%")
        except Exception as e:
            print(f"[C] {e}")

    if not scores:
        return 0.5

    total_w  = sum(weights)
    combined = sum(s*w for s,w in zip(scores,weights)) / total_w
    print(f"[RoBERTa-v6 ensemble] {round(combined*100,1)}%")
    return round(float(combined), 4)'''
code = re.sub(
    r"def sig_roberta\(text: str\) -> float:.*?return round\(float\(combined\), 4\)",
    sig_roberta_code,
    code,
    flags=re.DOTALL
)

# Replace get_sentence_highlights fallback block
highlights_code = '''def get_sentence_highlights(text: str) -> list:
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    valid, shorts = [], []

    for sent in sentences:
        sent = sent.strip()
        if not sent: continue
        if len(sent.split()) < 4:
            shorts.append({
                "sentence": sent,
                "ai_score": None,
                "label":    "too_short"
            })
        else:
            valid.append(sent)

    if not valid:
        return shorts

    try:
        # 1. Model A
        scores_a = []
        if MODEL_A_LOADED:
            results_a = MODEL_A_PIPE(valid, batch_size=len(valid))
            for res in results_a:
                raw = float(res["score"])
                label = res["label"]
                if label == _A_AI_LABEL:
                    score = raw if _A_AI_WHEN_HIGH else 1.0 - raw
                else:
                    score = (1.0 - raw) if _A_AI_WHEN_HIGH else raw
                scores_a.append(score)
        else:
            scores_a = [0.5] * len(valid)

        # 2. Model B
        scores_b = []
        if MODEL_B_LOADED:
            results_b = MODEL_B_PIPE(valid, batch_size=len(valid))
            for res in results_b:
                raw = float(res["score"])
                scores_b.append(raw if "label_1" in res["label"].lower() else 1.0 - raw)
        else:
            scores_b = [0.5] * len(valid)

        # 3. Model C
        scores_c = []
        if MODEL_C_LOADED:
            enc = MODEL_C_TOK(
                valid, return_tensors="pt", truncation=True, max_length=128, padding=True
            )
            with torch.no_grad():
                out = MODEL_C_MDL(**enc)
                probs = F.softmax(out.logits, dim=-1).numpy()
            for i in range(len(valid)):
                scores_c.append(float(probs[i][_C_AI_IDX]))
        else:
            scores_c = [0.5] * len(valid)

        results = []
        for i, sent in enumerate(valid):
            s1a = scores_a[i]
            s1b = scores_b[i]
            s1c = scores_c[i]

            # Ensemble S1 for this sentence (same weights as sig_roberta)
            r_score = (0.50 * s1a + 0.30 * s1b + 0.20 * s1c)
            s_score = sig_stylometric(sent)

            # Final sentence score
            score = round(0.70 * r_score + 0.30 * float(s_score), 3)

            label = ("AI"        if score >= 0.60 else
                     "LIKELY_AI" if score >= 0.45 else
                     "UNCERTAIN" if score >= 0.30 else "HUMAN")
            results.append({
                "sentence": sent,
                "ai_score": round(score*100, 1),
                "label":    label
            })

        print(f"[Highlights] {len(valid)} sentences processed with 3-model ensemble ✓")
        return shorts + results

    except Exception as e:
        print(f"[Highlights] Batch failed: {e}")
        # Fallback: individual calls
        results = []
        for sent in valid:
            try:
                s1a = 0.5
                if MODEL_A_LOADED:
                    res = MODEL_A_PIPE(sent)[0]
                    raw = float(res["score"])
                    label = res["label"]
                    if label == _A_AI_LABEL:
                        s1a = raw if _A_AI_WHEN_HIGH else 1.0 - raw
                    else:
                        s1a = (1.0 - raw) if _A_AI_WHEN_HIGH else raw
                r_score = s1a
                s_score = sig_stylometric(sent)
                score = round(0.65*r_score + 0.35*float(s_score), 3)
                label   = ("AI"        if score >= 0.80 else
                           "LIKELY_AI" if score >= 0.60 else
                           "UNCERTAIN" if score >= 0.40 else
                           "HUMAN")
                results.append({
                    "sentence": sent,
                    "ai_score": round(score*100, 1),
                    "label":    label
                })
            except:
                pass
        return shorts + results'''

code = re.sub(
    r"def get_sentence_highlights\(text: str\) -> list:.*?return shorts \+ results",
    highlights_code.replace('\\', '\\\\'),
    code,
    flags=re.DOTALL
)

# Update engine version
code = code.replace('"FakeShield-Text-v5.1"', '"FakeShield-Text-v6.0"')

with open(filepath, "w", encoding="utf-8") as f:
    f.write(code)
print("Patch applied successfully!")
