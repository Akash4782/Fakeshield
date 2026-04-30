import os
import sys
import time
from dotenv import load_dotenv

# FakeShield Industrial Verification Script v9.5
# Purpose: Validate end-to-end Tri-Vector pipeline and Gemini Reasoning.

load_dotenv()
sys.path.append(os.getcwd())

from app.models.new_forensic_engine import analyze_forensic

def verify():
    test_cases = [
        ("AI Generated (ChatGPT 4)", 
         "The rapid advancement of artificial intelligence has revolutionized various industries. "
         "By leveraging deep learning algorithms, organizations can now process vast amounts of data "
         "with unprecedented speed and accuracy. However, this transformation also raises important "
         "ethical considerations regarding privacy and job displacement."),
        
        ("Human Written (Casual)", 
         "I was just sitting at the park yesterday and realized how crazy life is. "
         "The birds were singing, people were laughing, and for a second, I forgot "
         "about all my deadlines. It's funny how a simple afternoon can change your "
         "entire mood. Sometimes you just need to breathe and let go.")
    ]

    print("\n" + "="*50)
    print(" FAKESHIELD INDUSTRIAL FORENSIC VALIDATION ")
    print("="*50 + "\n")

    for label, text in test_cases:
        print(f"Scanning: {label}")
        t0 = time.time()
        res = analyze_forensic(text)
        dt = time.time() - t0
        
        if "error" in res:
            print(f"FAILED: {res['error']}")
            continue

        # Format percentages safely (res['score'] is now 0-1)
        score_pct = res.get('score', 0) * 100
        conf_pct = res.get('confidence', 0) * 100
        
        print(f"Overall Prob: {score_pct:.2f}%")
        print(f"Verdict: {res['verdict']} ({conf_pct:.2f}%)")
        print(f"Threat Level: {res['threat_level']}")
        
        print("--- Full Signal Breakdown ---")
        signals = res.get('signals', {})
        for name, val in signals.items():
            print(f"{name.capitalize()}: {val}")
        
        print(f"Forensic Reasoning: {res.get('forensic_reasoning', 'N/A')}")
        print(f"Process Time: {dt:.2f}s\n")

    print("--- VERIFICATION COMPLETE ---")

if __name__ == "__main__":
    verify()
