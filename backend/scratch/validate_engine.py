"""
Quick validation: test AI-generated text through the live API
"""
import requests, json

AI_TEXT = """Machine learning is a subset of artificial intelligence that enables systems to learn and improve from experience without being explicitly programmed. It focuses on developing computer programs that can access data and use it to learn for themselves. The process begins with observations or data, such as examples, direct experience, or instruction, so that computers can learn to make better decisions based on the patterns they find in the data. The primary aim is to allow computers to learn automatically without human intervention or assistance and adjust actions accordingly. There are three main types of machine learning: supervised learning, unsupervised learning, and reinforcement learning. Supervised learning involves training a model on labeled data, where the correct answers are provided. Unsupervised learning deals with unlabeled data, and the model tries to find hidden patterns or intrinsic structures in the input. Reinforcement learning is based on rewarding desired behaviors and punishing undesired ones. Recommendation systems on platforms like Netflix or Spotify suggest content based on your behavior. Fraud detection systems in banks identify suspicious transactions. Virtual assistants, spam filters, self-driving cars, and medical diagnosis tools all rely heavily on machine learning models."""

HUMAN_TEXT = """I honestly couldn't sleep last night, kept tossing around this problem. Tried three different approaches and none of them really felt right. The third one was close, I mean it almost worked but then the edge cases just wrecked it. My friend suggested ignoring those cases entirely but that feels wrong. Anyway, I'm going back to basics tomorrow. Need coffee first though, it's been a rough week."""

BASE_URL = "http://localhost:8001"

def test(name, text):
    r = requests.post(f"{BASE_URL}/api/v1/text/analyze", json={"text": text, "mode": "deep"}, timeout=120)
    d = r.json()
    print(f"\n=== {name} ===")
    print(f"  Verdict:     {d.get('verdict')}")
    print(f"  AI Prob:     {d.get('score')}")
    print(f"  Threat:      {d.get('threat_level')}")
    print(f"  Confidence:  {d.get('confidence')}")
    sigs = d.get('signals', {})
    print(f"  DeBERTa:     {sigs.get('classifier_signal')}")
    print(f"  Human score raW: {d.get('linguistic_profile', {}).get('human_metrics')}")
    print(f"  AI score raw:    {d.get('linguistic_profile', {}).get('ai_metrics')}")

test("AI-GENERATED (ML explanation)", AI_TEXT)
test("HUMAN-WRITTEN (personal)", HUMAN_TEXT)
