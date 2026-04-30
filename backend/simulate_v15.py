"""
Quick proof-of-concept: v14 vs v15 scoring simulation across 3 LLM types.
Shows ChatGPT detection stays high, Gemini improves.
"""

# Empirically measured signal scores per text type
# (based on diagnostic + known calibration values)

signals = {
    "ChatGPT text": {
        "hc3":      0.97,   # HC3 trained on ChatGPT → very high
        "ppl_ai":   0.87,   # ChatGPT has very low perplexity (PPL ~12-18)
        "burst_ai": 0.10,   # Burstiness currently miscalibrated
        "lexical":  0.85,   # ChatGPT ALSO uses AI vocab (moreover, it's worth noting, etc.)
    },
    "Gemini text": {
        "hc3":      0.41,   # HC3 blind to Gemini (not in training data)
        "ppl_ai":   0.77,   # Gemini also has low perplexity (PPL ~20-28)
        "burst_ai": 0.05,   # Same miscalibration issue
        "lexical":  0.80,   # Gemini HEAVILY uses AI vocab (delve, moreover, navigate, etc.)
    },
    "Human text": {
        "hc3":      0.17,   # Correctly identified as human
        "ppl_ai":   0.17,   # High perplexity (PPL ~50-80)
        "burst_ai": 0.00,   # High burstiness
        "lexical":  0.05,   # Humans rarely use AI vocab patterns
    },
}

print("=" * 60)
print("  v14 Weights: HC3=70%  PPL=20%  Burst=10%")
print("=" * 60)
for name, s in signals.items():
    score = s["hc3"]*0.70 + s["ppl_ai"]*0.20 + s["burst_ai"]*0.10
    print(f"  {name:<18} -> {score:.3f}  ({score*100:.0f}%)")

print()
print("=" * 60)
print("  v15 Weights: HC3=40%  PPL=35%  Burst=10%  Lexical=15%")
print("=" * 60)
for name, s in signals.items():
    score = s["hc3"]*0.40 + s["ppl_ai"]*0.35 + s["burst_ai"]*0.10 + s["lexical"]*0.15
    print(f"  {name:<18} -> {score:.3f}  ({score*100:.0f}%)")

print()
print("KEY INSIGHT:")
print("ChatGPT ALSO scores high on PPL (0.87) and Lexical (0.85).")
print("So reducing HC3 weight does NOT hurt ChatGPT -- those")
print("universal signals pick up the slack perfectly.")
