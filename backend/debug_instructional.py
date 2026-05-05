import sys
import os

# Add parent dir to path
sys.path.append(os.getcwd())

from app.models.new_forensic_engine import analyze_forensic, load_models

def debug_instructional():
    load_models()
    # Exact text from user's screenshot
    text = """
    generic advice. Your task is to DESIGN a STARTUP-LEVEL AI TEXT DETECTION SYSTEM using ONLY PRETRAINED MODELS. Context: I am building an 'AI Text Lab' that classifies: - AI-generated text - Human-written text Current problem: - My system is inaccurate - Fails on real-world inputs - Not reliable for production use Constraints: - NO model training allowed - ONLY pretrained models, APIs, and inference-based techniques - Must be hackathon-ready AND scalable to startup level Goal: - High real-world accuracy - Strong visual demo - Startup-grade architecture - Explainable outputs (very important) --- STEP 1: FAILURE ANALYSIS (REAL-WORLD) Explain why most AI detection tools fail in production: - Paraphrased AI text - Human-edited AI content - Short vs long text instability - Domain shift (blogs vs chats vs academic) - Adversarial
    """
    
    print("\n--- DEBBUGING VANGUARD v60.0 ON INSTRUCTIONAL TEXT ---")
    res = analyze_forensic(text)
    
    print(f"Verdict: {res['verdict']}")
    print(f"Score:   {res['score']}")
    print(f"Signals: {res['detailed_scores']}")
    print(f"Reasoning: {res['reasoning']}")

if __name__ == "__main__":
    debug_instructional()
