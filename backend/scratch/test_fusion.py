"""
Fusion engine unit test — validates the fix without needing full model warmup
"""
import sys
sys.path.insert(0, ".")

from app.models.fusion_engine import FusionEngine

fe = FusionEngine()

# ─── Simulate the ACTUAL signals from diagnostic output ───
# (DeBERTa ~0.45, structural shows moderate human sigs, semantic moderate)

print("=" * 60)
print("FUSION ENGINE v12.0 — UNIT TESTS")
print("=" * 60)

# Test 1: AI-generated ML text (DeBERTa ~0.45, slight human structural)
signals_ai = {
    "classifier_signal":    0.45,   # DeBERTa - moderate AI signal
    "structural_strength":  0.54,
    "structural_uniformity": 0.61,
    "semantic_irregularity": 0.47,
    "semantic_uniformity":   0.66,
    "ppl_variation":         0.35,  # Low variation = AI smoothness
    "ppl_uniformity":        0.65,  # High uniformity = AI
}
r1 = fe.fuse(signals_ai, word_count=150)
print(f"\nTest 1 — AI ML explanation (DeBERTa=0.45, deberta moderate)")
print(f"  Verdict:   {r1['verdict']}")
print(f"  AI Prob:   {r1['ai_probability']}")
print(f"  Threat:    {r1['threat_level']}")
print(f"  Rule:      {r1['rule_applied']}")
print(f"  AI raw:    {round(r1['ai_score_raw'], 3)}")
print(f"  Human raw: {round(r1['human_score_raw'], 3)}")

# Test 2: Strong AI signal (DeBERTa 0.80)
signals_strong_ai = {
    "classifier_signal":    0.80,
    "structural_strength":  0.40,
    "structural_uniformity": 0.70,
    "semantic_irregularity": 0.35,
    "semantic_uniformity":   0.72,
    "ppl_variation":         0.20,
    "ppl_uniformity":        0.80,
}
r2 = fe.fuse(signals_strong_ai, word_count=200)
print(f"\nTest 2 — Strong AI (DeBERTa=0.80, veto expected)")
print(f"  Verdict:   {r2['verdict']}")
print(f"  AI Prob:   {r2['ai_probability']}")
print(f"  Rule:      {r2['rule_applied']}")

# Test 3: Clear human (DeBERTa 0.15, strong structural variation)
signals_human = {
    "classifier_signal":    0.15,
    "structural_strength":  0.75,
    "structural_uniformity": 0.25,
    "semantic_irregularity": 0.70,
    "semantic_uniformity":   0.30,
    "ppl_variation":         0.72,
    "ppl_uniformity":        0.28,
}
r3 = fe.fuse(signals_human, word_count=200)
print(f"\nTest 3 — Clear human (DeBERTa=0.15, strong human signals)")
print(f"  Verdict:   {r3['verdict']}")
print(f"  AI Prob:   {r3['ai_probability']}")
print(f"  Rule:      {r3['rule_applied']}")

# Test 4: Borderline (DeBERTa 0.55, mixed signals)
signals_borderline = {
    "classifier_signal":    0.55,
    "structural_strength":  0.50,
    "structural_uniformity": 0.50,
    "semantic_irregularity": 0.50,
    "semantic_uniformity":   0.50,
    "ppl_variation":         0.50,
    "ppl_uniformity":        0.50,
}
r4 = fe.fuse(signals_borderline, word_count=200)
print(f"\nTest 4 — Borderline (DeBERTa=0.55 as tiebreaker)")
print(f"  Verdict:   {r4['verdict']}")
print(f"  AI Prob:   {r4['ai_probability']}")
print(f"  Rule:      {r4['rule_applied']}")
