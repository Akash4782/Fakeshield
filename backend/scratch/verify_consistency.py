import sys
import os
import time

# Add parent dir to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

try:
    from app.models.new_forensic_engine import analyze_forensic, load_models
except ImportError as e:
    print(f"Import error: {e}")
    sys.exit(1)

# Ensure models are loaded
load_models()

human_text = """Machine learning is a branch of Artificial Intelligence that focuses on building systems that can learn from data instead of being explicitly programmed with fixed rules. In traditional programming, you write step-by-step instructions to solve a problem, but in machine learning, you feed a system large amounts of data and allow it to identify patterns, relationships, and structures on its own. Over time, the system improves its performance as it processes more data, making it "learn" from experience. This is why machine learning is considered a data-driven approach—its effectiveness depends heavily on the quality and quantity of data available. At its core, machine learning works by creating mathematical models that map inputs to outputs. These models are trained using algorithms that adjust internal parameters to minimize errors between predicted and actual results. For example, if you want a system to recognize whether an email is spam or not, you provide it with many examples of emails labeled as spam or not spam. The model analyzes features like keywords, frequency, and patterns, and gradually learns how to classify new, unseen emails correctly. This learning process is called "training," and once trained, the model can make predictions or decisions without human intervention. Machine learning can be broadly divided into..."""

def verify_consistency():
    print("Verifying Heatmap Consistency on Human-leaning text...")
    
    t0 = time.time()
    result = analyze_forensic(human_text)
    t1 = time.time()
    
    print(f"\nVerdict: {result['verdict']} ({result['confidence']}%)")
    print(f"Processing Time: {t1-t0:.2f}s")
    
    highlights = result['sentence_highlights']
    num_ai = sum(1 for h in highlights if h['label'] in ('AI', 'LIKELY_AI'))
    total_valid = sum(1 for h in highlights if h['label'] != 'too_short')
    
    print(f"AI Highlights: {num_ai} / {total_valid} sentences")
    
    if num_ai > (total_valid * 0.3) and result['verdict'] == 'LIKELY HUMAN':
        print("\nWARNING: Still seeing high AI highlights on Human verdict text.")
    else:
        print("\nSUCCESS: Heatmap consistency is high.")

if __name__ == "__main__":
    verify_consistency()
