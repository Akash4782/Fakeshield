"""
Full failure-case analysis across all 5 text scenarios.
Shows where each approach breaks down.
"""

# Measured/estimated signal scores for each text type
scenarios = {
    "ChatGPT (formal/technical)": {
        "hc3": 0.97, "ppl_ai": 0.87, "burst_ai": 0.05, "lexical": 0.85,
        "expected": "AI", "note": "Easy case — all signals agree"
    },
    "ChatGPT (casual/conversational)": {
        "hc3": 0.52, "ppl_ai": 0.74, "burst_ai": 0.04, "lexical": 0.60,
        "expected": "AI", "note": "HC3 drops when ChatGPT writes casually"
    },
    "ChatGPT (with noise/edits)": {
        "hc3": 0.58, "ppl_ai": 0.69, "burst_ai": 0.05, "lexical": 0.65,
        "expected": "AI", "note": "Partially edited ChatGPT output"
    },
    "Gemini (formal)": {
        "hc3": 0.41, "ppl_ai": 0.77, "burst_ai": 0.04, "lexical": 0.80,
        "expected": "AI", "note": "HC3 blind to Gemini architecture"
    },
    "Human (academic style)": {
        "hc3": 0.38, "ppl_ai": 0.28, "burst_ai": 0.02, "lexical": 0.15,
        "expected": "HUMAN", "note": "Formal human writing — must NOT flag"
    },
    "Human (casual)": {
        "hc3": 0.17, "ppl_ai": 0.15, "burst_ai": 0.01, "lexical": 0.04,
        "expected": "HUMAN", "note": "Easy case — clearly human"
    },
}

def verdict(score):
    if score >= 0.60: return "AI GENERATED"
    elif score >= 0.45: return "UNCERTAIN"
    else: return "LIKELY HUMAN"

def ok(name, score, expected):
    v = verdict(score)
    correct = ("AI" in v and expected == "AI") or (v == "LIKELY HUMAN" and expected == "HUMAN")
    return "OK" if correct else "WRONG"

# ── v14: HC3=70% PPL=20% Burst=10%
print("\n=== v14 (Current): HC3=70%  PPL=20%  Burst=10% ===\n")
print(f"  {'Scenario':<35} {'Score':>6}  {'Verdict':<14}  {'Status'}")
print("  " + "-"*75)
for name, s in scenarios.items():
    score = s["hc3"]*0.70 + s["ppl_ai"]*0.20 + s["burst_ai"]*0.10
    status = ok(name, score, s["expected"])
    flag = "  <-- FAIL" if status == "WRONG" or (verdict(score) == "UNCERTAIN" and s["expected"] == "AI") else ""
    print(f"  {name:<35} {score:>6.3f}  {verdict(score):<14}  {status}{flag}")

# ── v15a: Simple reweight HC3=40% PPL=35% Burst=10% Lexical=15%
print("\n=== v15a (Simple Reweight): HC3=40%  PPL=35%  Burst=10%  Lexical=15% ===\n")
print(f"  {'Scenario':<35} {'Score':>6}  {'Verdict':<14}  {'Status'}")
print("  " + "-"*75)
for name, s in scenarios.items():
    score = s["hc3"]*0.40 + s["ppl_ai"]*0.35 + s["burst_ai"]*0.10 + s["lexical"]*0.15
    status = ok(name, score, s["expected"])
    flag = "  <-- FAIL" if status == "WRONG" or (verdict(score) == "UNCERTAIN" and s["expected"] == "AI") else ""
    print(f"  {name:<35} {score:>6.3f}  {verdict(score):<14}  {status}{flag}")

# ── v15b: Adaptive — HC3 strong? trust it. HC3 weak? boost PPL+Lexical
print("\n=== v15b (ADAPTIVE - BEST): Base v14 + Gemini Boost when HC3 uncertain ===\n")
print(f"  {'Scenario':<35} {'Score':>6}  {'Verdict':<14}  {'Status'}")
print("  " + "-"*75)
for name, s in scenarios.items():
    # Base: same as v14
    base = s["hc3"]*0.70 + s["ppl_ai"]*0.20 + s["burst_ai"]*0.10

    # If HC3 is uncertain (0.35-0.65) but PPL or Lexical is strong -> apply boost
    hc3 = s["hc3"]
    ppl = s["ppl_ai"]
    lex = s["lexical"]

    boost = 0.0
    if 0.35 <= hc3 <= 0.65:   # HC3 uncertain zone
        stat_strength = ppl * 0.60 + lex * 0.40
        if stat_strength > 0.55:  # Statistical signals say AI
            boost = (stat_strength - 0.55) * 0.60  # proportional boost

    score = min(base + boost, 1.0)
    status = ok(name, score, s["expected"])
    flag = "  <-- FAIL" if status == "WRONG" or (verdict(score) == "UNCERTAIN" and s["expected"] == "AI") else ""
    boost_str = f"  [+{boost:.3f} boost]" if boost > 0 else ""
    print(f"  {name:<35} {score:>6.3f}  {verdict(score):<14}  {status}{boost_str}{flag}")

print("\n")
print("KEY: v15b (Adaptive) applies a boost ONLY when HC3 is uncertain.")
print("  - ChatGPT formal:     HC3=0.97 -> confident -> no boost -> unchanged")
print("  - ChatGPT casual:     HC3=0.52 -> uncertain -> PPL+Lexical boost -> improves")
print("  - Gemini:             HC3=0.41 -> uncertain -> PPL+Lexical boost -> improves")
print("  - Human academic:     HC3=0.38 -> uncertain BUT PPL=0.28 (low) -> no boost -> safe")
print("  - Human casual:       HC3=0.17 -> confident human -> no boost -> safe")
