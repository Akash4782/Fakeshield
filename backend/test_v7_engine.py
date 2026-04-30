import sys
import os
import json

# Add parent dir to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from app.models.new_forensic_engine import analyze_forensic
except ImportError as e:
    print(f"Import error: {e}")
    sys.exit(1)

# Test texts
ai_text = """Artificial intelligence (AI) is transforming the way we live and work. In conclusion, it is worth noting that machine learning algorithms can process vast amounts of data to provide actionable insights. Furthermore, the integration of AI into various industries has led to significant improvements in efficiency and productivity. It is imperative that we consider the ethical implications of this technology as we move forward in this rapidly evolving landscape."""

human_text = """I was walking down the street yesterday and saw this really weird cat. It had like three different colors and was wearing a tiny hat. Honestly, I didn't know what to think. I tried to take a picture but it ran away before I could get my phone out. Just my luck, right? Anyway, I'm heading over to my friend's house now to tell her about it. She loves cats but she probably won't believe me about the hat."""

def test_engine(text, label):
    print(f"\n--- Testing {label} Text ---")
    result = analyze_forensic(text)
    
    if "error" in result:
        print(f"Error: {result['error']}")
        return

    print(f"Verdict: {result['verdict']}")
    print(f"Confidence: {result['confidence']}% ({result['confidence_level']})")
    print(f"Agreement: {result['agreement_score']}")
    print(f"Fusion Rule: {result['fusion_details']['rule_applied']}")
    
    print("\nReasons:")
    for reason in result.get('reasons', []):
        print(f"  - {reason}")
    
    print("\nIndicators:")
    for ind in result.get('indicators', []):
        print(f"  - {ind}")

print("FakeShield v7.0 Forensic Engine Test")
test_engine(ai_text, "AI")
test_engine(human_text, "Human")
