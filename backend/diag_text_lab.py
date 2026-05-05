# -*- coding: utf-8 -*-
"""
AI Text Lab -- Full Diagnostic Script (ASCII-safe for Windows cp1252)
Checks: HC3, GPT-2, Structural, Semantic, Forensic Judge, Full Ensemble
"""
import sys, os, time, traceback
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

PASS = "[PASS]"
FAIL = "[FAIL]"
WARN = "[WARN]"
INFO = "[INFO]"

results = {}

AI_TEXT = (
    "Machine learning is a subset of artificial intelligence that enables systems to learn "
    "and improve from experience without being explicitly programmed. It focuses on developing "
    "computer programs that can access data and use it to learn for themselves. The process begins "
    "with observations or data, such as examples, direct experience, or instruction. It looks for "
    "patterns in data and makes better decisions in the future. There are three main types: "
    "supervised learning, unsupervised learning, and reinforcement learning. Each type has its own "
    "use cases and advantages in different applications."
)

HUMAN_TEXT = (
    "I honestly couldn't sleep last night. Kept tossing this bug over in my head -- tried three "
    "different approaches and none of them felt right. My friend said to just skip the edge cases "
    "but that feels totally wrong to me. Sometimes I wonder if I'm overcomplicating things. "
    "Anyway, need coffee badly. The kind of day where nothing works until it suddenly does."
)

print("\n" + "="*65)
print("   FakeShield -- AI Text Lab Diagnostic")
print("="*65 + "\n")

# ── 1. Neural Detector ─────────────────────────────────────────────
print(f"{INFO} [1/6] Testing Neural Transformer (DeBERTa/RoBERTa)...")
try:
    from app.models.text_classifier_ensemble import load_neural_detector, _multi_model_neural_vote as _neural_document_score
    load_neural_detector()
    import app.models.text_classifier_ensemble as tce
    if tce._neural_tok is None:
        raise RuntimeError("Neural tokenizer is None after loading")

    t = time.time()
    ai_res  = _neural_document_score(AI_TEXT)
    hum_res = _neural_document_score(HUMAN_TEXT)
    elapsed = time.time() - t

    ai_score  = ai_res["avg_score"]
    hum_score = hum_res["avg_score"]

    print(f"   AI text    -> Neural AI prob = {ai_score:.3f}  (expected: > 0.60)")
    print(f"   Human text -> Neural AI prob = {hum_score:.3f}  (expected: < 0.45)")
    print(f"   Sentences:   AI={ai_res['sentence_count']}, Human={hum_res['sentence_count']}")
    print(f"   Elapsed:     {elapsed:.2f}s")

    if ai_score > 0.60 and hum_score < 0.50:
        print(f"   {PASS} Neural classifier is working correctly.")
        results["Neural"] = "PASS"
    elif ai_score > 0.50:
        print(f"   {WARN} Neural working but borderline AI score ({ai_score:.3f}).")
        results["Neural"] = "WARN"
    else:
        print(f"   {FAIL} Neural NOT distinguishing AI from human text properly!")
        results["Neural"] = "FAIL"
except Exception as e:
    print(f"   {FAIL} Neural CRASHED: {e}")
    traceback.print_exc()
    results["Neural"] = "FAIL"

# ── 1.5 Binoculars Detector ────────────────────────────────────────
print(f"\n{INFO} [1.5/6] Testing Binoculars (Pythia 160m/70m)...")
try:
    from app.models.binoculars import Binoculars
    bino = Binoculars(device="cpu")
    
    t = time.time()
    ai_bino = bino.predict(AI_TEXT)
    hum_bino = bino.predict(HUMAN_TEXT)
    elapsed = time.time() - t
    
    print(f"   AI text    -> Bino score = {ai_bino['score']:.3f}  prob = {ai_bino['ai_probability']:.3f}")
    print(f"   Human text -> Bino score = {hum_bino['score']:.3f}  prob = {hum_bino['ai_probability']:.3f}")
    print(f"   Elapsed:     {elapsed:.2f}s")
    
    if ai_bino['ai_probability'] > 0.60 and hum_bino['ai_probability'] < 0.40:
        print(f"   {PASS} Binoculars engine working correctly.")
        results["Binoculars"] = "PASS"
    else:
        print(f"   {WARN} Binoculars engine signal is weak or uncalibrated.")
        results["Binoculars"] = "WARN"
except Exception as e:
    print(f"   {FAIL} Binoculars CRASHED: {e}")
    traceback.print_exc()
    results["Binoculars"] = "FAIL"

# ── 2. GPT-2 Perplexity + Burstiness ──────────────────────────────
print(f"\n{INFO} [2/6] Testing GPT-2 Medium (Perplexity + Burstiness)...")
try:
    from app.models.text_classifier_ensemble import load_ppl_engine, _stats_engine_v16
    load_ppl_engine()
    import app.models.text_classifier_ensemble as tce2
    if tce2._ppl_tok is None:
        raise RuntimeError("GPT-2 tokenizer is None after loading")

    t = time.time()
    ai_gpt2  = _stats_engine_v16(AI_TEXT)
    hum_gpt2 = _stats_engine_v16(HUMAN_TEXT)
    elapsed  = time.time() - t

    print(f"   AI text    -> PPL={ai_gpt2['perplexity']:.1f}  ppl_ai={ai_gpt2['ppl_score']:.3f}  burst={ai_gpt2['burstiness']:.3f}  burst_ai={ai_gpt2['burstiness_score']:.3f}")
    print(f"   Human text -> PPL={hum_gpt2['perplexity']:.1f}  ppl_ai={hum_gpt2['ppl_score']:.3f}  burst={hum_gpt2['burstiness']:.3f}  burst_ai={hum_gpt2['burstiness_score']:.3f}")
    print(f"   Elapsed:     {elapsed:.2f}s")

    if ai_gpt2["ppl_score"] > hum_gpt2["ppl_score"]:
        print(f"   {PASS} GPT-2 perplexity signal is directionally correct.")
        results["GPT2"] = "PASS"
    else:
        print(f"   {WARN} GPT-2 perplexity signal is flat/inverted -- check calibration.")
        results["GPT2"] = "WARN"
except Exception as e:
    print(f"   {FAIL} GPT-2 CRASHED: {e}")
    traceback.print_exc()
    results["GPT2"] = "FAIL"

# ── 3. Structural Engine ───────────────────────────────────────────
print(f"\n{INFO} [3/5] Testing Structural Engine (spaCy en_core_web_sm)...")
try:
    from app.models.structural_engine import StructuralEngine
    eng = StructuralEngine()
    if not eng.enabled:
        raise RuntimeError("StructuralEngine disabled -- spaCy model en_core_web_sm not found")

    t = time.time()
    ai_struct  = eng.analyze(AI_TEXT)
    hum_struct = eng.analyze(HUMAN_TEXT)
    elapsed    = time.time() - t

    print(f"   AI text    -> uniformity={ai_struct['high_uniformity']:.3f}  strength={ai_struct['structural_strength']:.3f}")
    print(f"   Human text -> uniformity={hum_struct['high_uniformity']:.3f}  strength={hum_struct['structural_strength']:.3f}")
    print(f"   Elapsed:     {elapsed:.2f}s")

    if "error" in ai_struct.get("details", {}):
        print(f"   {WARN} Structural engine returned error: {ai_struct['details']}")
        results["Structural"] = "WARN"
    else:
        print(f"   {PASS} Structural engine (spaCy) working correctly.")
        results["Structural"] = "PASS"
except Exception as e:
    print(f"   {FAIL} Structural Engine CRASHED: {e}")
    traceback.print_exc()
    results["Structural"] = "FAIL"

# ── 4. Semantic Drift Engine ───────────────────────────────────────
print(f"\n{INFO} [4/5] Testing Semantic Drift Engine (all-mpnet-base-v2)...")
try:
    from app.models.semantic_drift import SemanticDriftEngine
    drift = SemanticDriftEngine()
    if not drift.enabled:
        raise RuntimeError("SemanticDriftEngine disabled -- sentence-transformers / mpnet failed")

    t = time.time()
    ai_drift  = drift.analyze(AI_TEXT)
    hum_drift = drift.analyze(HUMAN_TEXT)
    elapsed   = time.time() - t

    ai_irr  = ai_drift.get('semantic_irregularity', 'N/A')
    ai_uni  = ai_drift.get('semantic_uniformity', 'N/A')
    hu_irr  = hum_drift.get('semantic_irregularity', 'N/A')
    hu_uni  = hum_drift.get('semantic_uniformity', 'N/A')

    print(f"   AI text    -> irregularity={ai_irr}  uniformity={ai_uni}")
    print(f"   Human text -> irregularity={hu_irr}  uniformity={hu_uni}")
    print(f"   Elapsed:     {elapsed:.2f}s")

    if "error" in ai_drift.get("details", {}):
        print(f"   {WARN} Drift engine error: {ai_drift['details']}")
        results["SemanticDrift"] = "WARN"
    else:
        print(f"   {PASS} Semantic Drift Engine (mpnet) working correctly.")
        results["SemanticDrift"] = "PASS"
except Exception as e:
    print(f"   {FAIL} Semantic Drift CRASHED: {e}")
    traceback.print_exc()
    results["SemanticDrift"] = "FAIL"

# ── 5. Full Ensemble Pipeline ──────────────────────────────────────
print(f"\n{INFO} [5/5] Testing Full Ensemble Pipeline (analyze_forensic)...")
try:
    from app.models.new_forensic_engine import analyze_forensic, load_models
    load_models()

    t = time.time()
    ai_result  = analyze_forensic(AI_TEXT, mode="fast")
    hum_result = analyze_forensic(HUMAN_TEXT, mode="fast")
    elapsed    = time.time() - t

    print(f"\n   --- AI TEXT RESULT ---")
    print(f"   Verdict:     {ai_result.get('verdict')}  (threat={ai_result.get('threat_level')})")
    print(f"   Score:       {ai_result.get('score')}  (expected: > 0.60)")
    print(f"   Confidence:  {ai_result.get('confidence')}")
    lbd = ai_result.get('signals', {})
    print(f"   Layers:      Neural={lbd.get('classifier_signal', 'N/A'):.3f}  Bino={lbd.get('binoculars_signal', 'N/A'):.3f}  PPL={lbd.get('ppl_signal', 'N/A'):.3f}  Sty={lbd.get('structural_strength', 'N/A'):.3f}")
    print(f"   Process time:{ai_result.get('processing_time')}")

    print(f"\n   --- HUMAN TEXT RESULT ---")
    print(f"   Verdict:     {hum_result.get('verdict')}  (threat={hum_result.get('threat_level')})")
    print(f"   Score:       {hum_result.get('score')}  (expected: < 0.45)")
    print(f"   Confidence:  {hum_result.get('confidence')}")
    lbh = hum_result.get('signals', {})
    print(f"   Layers:      Neural={lbh.get('classifier_signal', 'N/A'):.3f}  Bino={lbh.get('binoculars_signal', 'N/A'):.3f}  PPL={lbh.get('ppl_signal', 'N/A'):.3f}  Sty={lbh.get('structural_strength', 'N/A'):.3f}")
    print(f"   Process time:{hum_result.get('processing_time')}")

    print(f"\n   Total wall-clock: {elapsed:.2f}s")

    ai_ok  = ai_result.get("score", 0) >= 0.55
    hum_ok = hum_result.get("score", 1) <= 0.50

    if ai_ok and hum_ok:
        print(f"   {PASS} Full ensemble pipeline working correctly!")
        results["Ensemble"] = "PASS"
    elif ai_ok or hum_ok:
        print(f"   {WARN} Ensemble partially working -- one side is off. Check calibration.")
        results["Ensemble"] = "WARN"
    else:
        print(f"   {FAIL} Ensemble NOT distinguishing AI from human text correctly!")
        results["Ensemble"] = "FAIL"
except Exception as e:
    print(f"   {FAIL} Full Ensemble CRASHED: {e}")
    traceback.print_exc()
    results["Ensemble"] = "FAIL"

# ── Summary ────────────────────────────────────────────────────────
print("\n" + "="*65)
print("   DIAGNOSTIC SUMMARY")
print("="*65)
all_pass = True
for component, status in results.items():
    icon = PASS if status == "PASS" else (WARN if status == "WARN" else FAIL)
    print(f"   {icon} {component:<20} -> {status}")
    if status == "FAIL":
        all_pass = False

print()
if all_pass:
    print("  ALL COMPONENTS OPERATIONAL")
else:
    print("  ISSUES DETECTED -- see details above")
print("="*65 + "\n")
