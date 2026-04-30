# -*- coding: utf-8 -*-
"""
v15b Verification — tests all 4 critical text types.
Gemini, ChatGPT formal, ChatGPT casual, Human text.
"""
import sys, os, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.models.new_forensic_engine import load_models, analyze_forensic

load_models()

TEXTS = {
    "Gemini (formal/academic)": (
        "Artificial intelligence is fundamentally transforming the landscape of modern "
        "industries. It is worth noting that machine learning, at its core, enables systems "
        "to learn from data and improve over time without explicit programming. Furthermore, "
        "there are several key aspects to consider when evaluating AI adoption. In essence, "
        "organizations must leverage these technologies to remain competitive. This enables "
        "a more comprehensive approach to data-driven decision making. In conclusion, AI "
        "represents a pivotal shift in how we navigate complex problems.",
        "AI"
    ),
    "ChatGPT (formal/technical)": (
        "Machine learning is a subset of artificial intelligence that enables systems to learn "
        "and improve from experience without being explicitly programmed. It focuses on developing "
        "computer programs that can access data and use it to learn for themselves. The process "
        "begins with observations or data such as examples, direct experience, or instruction. "
        "It looks for patterns in data and makes better decisions in the future. There are three "
        "main types: supervised learning, unsupervised learning, and reinforcement learning. "
        "Each type has its own use cases and advantages in different applications.",
        "AI"
    ),
    "ChatGPT (casual/conversational)": (
        "So I was thinking about how AI actually works and it's pretty cool honestly. "
        "Like, the model just looks at tons of data and learns patterns from it. "
        "It doesn't actually understand anything the way humans do, but it can seem "
        "like it does because it got really good at predicting what comes next. "
        "When it comes to everyday use, AI tools are becoming more common. "
        "Overall, it's a fascinating area that continues to grow rapidly.",
        "AI"
    ),
    "Human (casual/authentic)": (
        "I honestly couldn't sleep last night. Kept tossing this bug over in my head -- "
        "tried three different approaches and none of them felt right. My friend said to "
        "just skip the edge cases but that feels totally wrong to me. Sometimes I wonder "
        "if I'm overcomplicating things. Anyway, need coffee badly. The kind of day where "
        "nothing works until it suddenly does.",
        "HUMAN"
    ),
}

print("\n" + "="*70)
print("   FakeShield v15b Adaptive Boost -- Verification Run")
print("="*70)

all_pass = True
for name, (text, expected) in TEXTS.items():
    t = time.time()
    r = analyze_forensic(text, mode="fast")
    elapsed = time.time() - t

    score   = r.get("score", 0)
    verdict = r.get("verdict", "?")
    lbd     = r.get("layer_breakdown", {})
    raw     = r.get("raw_metrics", {})
    boost   = raw.get("boost_applied", False)
    boost_v = raw.get("boost_amount", 0.0)
    lex     = lbd.get("lexical_ai_score", 0.0)

    is_ai   = score >= 0.55
    correct = (is_ai and expected == "AI") or (not is_ai and expected == "HUMAN")
    status  = "[PASS]" if correct else "[FAIL]"
    if not correct:
        all_pass = False

    boost_tag = f"  [BOOST +{boost_v:.3f}]" if boost else ""

    print(f"\n  {status} {name}")
    print(f"         Score:   {score:.3f} ({int(score*100)}%)  Verdict: {verdict}")
    print(f"         HC3:     {lbd.get('hc3_chatgpt_detector', 0):.3f}  "
          f"PPL: {lbd.get('gpt2_perplexity', 0):.3f}  "
          f"Lexical: {lex:.3f}{boost_tag}")
    print(f"         Expected: {expected}  |  Time: {elapsed:.2f}s")

print("\n" + "="*70)
if all_pass:
    print("  ALL TESTS PASSED -- v15b is working correctly.")
else:
    print("  SOME TESTS FAILED -- review output above.")
print("="*70 + "\n")
