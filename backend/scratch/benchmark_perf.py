import time
import sys
import os

# Add the project root to sys.path
sys.path.append(os.getcwd())

from app.models.new_forensic_engine import load_models, analyze_forensic
from app.models.text_classifier_ensemble import ensemble_predict, ensemble_predict_sentences

def benchmark():
    print("Warmup: Loading models...", flush=True)
    load_models()
    
    text = """
The impact of artificial intelligence on modern society is profound and multi-faceted. AI technologies are increasingly integrated into various sectors, including healthcare, finance, and education. In healthcare, AI-driven diagnostic tools are enhancing the accuracy and speed of identifying diseases, leading to better patient outcomes. Financial institutions leverage AI for fraud detection and risk management, optimizing their operations and safeguarding customer assets. In the field of education, personalized learning platforms powered by AI are tailoring educational content to meet the unique needs of individual students. However, the rapid advancement of AI also raises ethical concerns regarding privacy, bias, and job displacement. It is crucial for policymakers and developers to work together to ensure that AI is developed and deployed responsibly. As we move forward, the continued evolution of AI will undoubtedly shape the future of humanity in ways we are only beginning to understand. The integration of AI in everyday life is not just a technological shift but a societal transformation that requires careful consideration and proactive management to maximize benefits and mitigate risks.
"""
    # approx 10 sentences
    
    print("\n--- Document Analysis Benchmark ---", flush=True)
    start = time.time()
    res = ensemble_predict(text)
    end = time.time()
    print(f"ensemble_predict took: {end-start:.4f}s", flush=True)
    
    sentences = res["_neural_internal"]["sentences"]
    layers = res["layer_scores"]
    
    print(f"\n--- Sentence Highlights Benchmark ({len(sentences)} sentences) ---", flush=True)
    start = time.time()
    sent_res = ensemble_predict_sentences(sentences, doc_context=layers)
    end = time.time()
    print(f"ensemble_predict_sentences took: {end-start:.4f}s", flush=True)
    print(f"Avg time per sentence: {(end-start)/len(sentences):.4f}s", flush=True)

if __name__ == "__main__":
    benchmark()
