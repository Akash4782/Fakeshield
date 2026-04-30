import sys
import os
import time
import torch

# Add parent dir to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

try:
    from app.models.new_forensic_engine import analyze_forensic, load_models
    import app.models.new_forensic_engine as engine
except ImportError as e:
    print(f"Import error: {e}")
    sys.exit(1)

# Ensure models are loaded
load_models()

ai_text = """Artificial intelligence (AI) refers to the simulation of human intelligence processes by machines, especially computer systems. These processes include learning (the acquisition of information and rules for using the information), reasoning (using rules to reach approximate or definite conclusions) and self-correction. Particular applications of AI include expert systems, speech recognition and machine vision.

Machine learning is a subset of AI that focuses on the use of data and algorithms to imitate the way that humans learn, gradually improving its accuracy. In conclusion, it is worth noting that deep learning is a specialized branch of machine learning that focuses on training neural networks. These models automatically learn features from raw data, making them highly effective across various industries."""

def benchmark():
    print(f"Benchmarking Test Lab on Device: {engine.DEVICE}")
    print(f"Text length: {len(ai_text)} chars, {len(ai_text.split())} words")
    
    start_total = time.time()
    result = analyze_forensic(ai_text)
    end_total = time.time()
    
    print("\n--- PERFORMANCE SUMMARY ---")
    print(f"Total processing time: {end_total - start_total:.2f}s")
    print(f"Reported processing_time: {result['processing_time']}")
    print(f"Num sentences: {result['sentence_count']}")
    
    # We want to know how much time was spent on sentences
    # Since we can't easily hook into the function without modifying it,
    # let's just observe the total.
    
    print("\n--- VERDICT ---")
    print(f"Verdict: {result['verdict']} ({result['confidence']}%)")
    
    print("\n--- SENTENCE HIGHLIGHTS ---")
    for i, h in enumerate(result['sentence_highlights']):
        print(f"S{i+1}: [{h['label']}] ({h.get('ai_score', 'N/A')}%) {h['sentence'][:50]}...")

if __name__ == "__main__":
    benchmark()
