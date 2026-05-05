import sys, os, time
import numpy as np
from typing import Dict, Any

# Ensure backend path is in sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.models.new_forensic_engine import analyze_forensic, load_models

# --- DATASET PREPARATION (LONG SAMPLES > 120 WORDS) ---

SAMPLES = {
    "Wikipedia (Human)": {
        "text": """A large language model (LLM) is a type of artificial intelligence (AI) program that can recognize and generate text, among other tasks. LLMs are trained on immense datasets—hence the 'large' in their name—and are built on neural networks, specifically transformer architectures. These models have revolutionized the field of natural language processing (NLP), enabling applications like chatbots, automated translation, and complex data summarization. By analyzing billions of parameters, LLMs can predict the next word in a sequence with remarkable accuracy, allowing them to produce coherent and contextually relevant prose that often mimics human writing styles. However, the development and deployment of these models come with significant ethical and technical challenges. Concerns about bias in training data, the potential for generating misinformation, and the sheer computational power required for training are central topics in AI research today. As of 2024, the most advanced LLMs, such as GPT-4 and Gemini, are being integrated into professional workflows across diverse industries, from software development to creative writing, fundamentally altering how humans interact with digital information and machine-generated content. Despite their prowess, these models are not truly 'intelligent' in the human sense; they are statistical engines that map linguistic patterns without an internal understanding of the concepts they discuss.""",
        "expected": "HUMAN"
    },
    "Wikipedia (AI)": {
        "text": """Large language models (LLMs) represent a transformative advancement in the domain of artificial intelligence, particularly within the branch of natural language processing. These sophisticated systems are engineered to understand, interpret, and generate human-like text by processing vast quantities of data. At their core, LLMs utilize deep learning techniques and are predominantly based on the transformer architecture, which facilitates the handling of long-range dependencies in language. This architectural design enables the models to perform a wide array of tasks, including language translation, sentiment analysis, and the creation of highly detailed content. The training process involves exposing the model to massive corpora of text, allowing it to learn the statistical relationships between words and phrases. While the capabilities of modern LLMs are impressive, they are also subject to limitations such as hallucinations, where the model generates factually incorrect information with high confidence. Furthermore, the environmental impact of training these massive models has become a point of significant discussion in the tech community. As the technology continues to evolve, researchers are focusing on making these models more efficient, safer, and better aligned with human values and factual accuracy across all domains.""",
        "expected": "AI"
    },
    "Research (Human)": {
        "text": """The dominant sequence transduction models are based on complex recurrent or convolutional neural networks in an encoder-decoder configuration. The best performing models also connect the encoder and decoder through an attention mechanism. We propose a new simple network architecture, the Transformer, based solely on attention mechanisms, dispensing with recurrence and convolutions entirely. Experiments on two machine translation tasks show these models to be superior in quality while being more parallelizable and requiring significantly less time to train. Our model achieves 28.4 BLEU on the WMT 2014 English-to-German translation task, improving over the existing best results, including ensembles by over 2 BLEU. On the WMT 2014 English-to-French translation task, our model establishes a new single-model state-of-the-art BLEU score of 41.8 after training for 3.5 days on eight GPUs, a small fraction of the training costs of the best models from the literature. We show that the Transformer generalizes well to other tasks by applying it successfully to English constituency parsing both with large and limited training data. This architecture represents a significant shift away from sequential processing, allowing for massive increases in training efficiency and the ability to capture global dependencies within the input data without the constraints of traditional recurrent layers.""",
        "expected": "HUMAN"
    },
    "Research (AI)": {
        "text": """Recent advancements in the field of sequence modeling have witnessed a significant transition from traditional recurrent and convolutional architectures toward attention-based frameworks. This shift is primarily driven by the need for enhanced parallelization and the ability to model long-range dependencies more effectively. To address these requirements, we introduce the Transformer, a novel architectural design that relies exclusively on self-attention mechanisms to calculate representations of its input and output. Unlike previous models that process tokens sequentially, the Transformer allows for simultaneous processing of entire sequences, which drastically reduces training times while maintaining high levels of performance. Our empirical evaluations across several machine translation benchmarks, including the WMT 2014 English-to-German dataset, demonstrate that the Transformer consistently outperforms existing state-of-the-art models. Additionally, we observe that the self-attention mechanism provides interpretable insights into how the model assigns importance to different parts of the input sequence. The scalability of this architecture suggests its applicability to a broad range of tasks beyond translation, such as document summarization and image generation, marking a pivotal moment in the evolution of deep learning for complex linguistic structures.""",
        "expected": "AI"
    }
}

def run_validation():
    print("\n" + "="*70)
    print("   FAKESHIELD V26 STARTUP-GRADE VALIDATION (v2)")
    print("   Testing Human vs AI across: Wikipedia, Blogs, Research")
    print("   ENFORCING >120 WORD COUNT FOR ELITE ANALYSIS")
    print("="*70 + "\n")

    print("[SYSTEM] Loading Startup-Grade Forensic Suite...")
    load_models()
    print("[SYSTEM] Warmup complete. Beginning audit.\n")

    results = []
    
    for name, data in SAMPLES.items():
        word_count = len(data["text"].split())
        print(f"[AUDIT] Processing: {name} ({word_count} words)...", end="", flush=True)
        t0 = time.time()
        res = analyze_forensic(data["text"], mode="deep")
        elapsed = time.time() - t0
        
        score = res.get("score", 0.5)
        verdict = res.get("verdict", "N/A")
        
        # Check if verdict matches expectation
        success = False
        if data["expected"] == "AI" and score > 0.50: success = True
        if data["expected"] == "HUMAN" and score < 0.50: success = True
        
        results.append({
            "name": name,
            "expected": data["expected"],
            "score": score,
            "verdict": verdict,
            "success": success,
            "time": elapsed,
            "signals": res.get("signals", {}),
            "reasoning": res.get("forensic_reasoning", "N/A")
        })
        print(f" DONE ({elapsed:.2f}s)")

    # --- REPORT TABLE ---
    print("\n" + "="*70)
    print(f"{'SAMPLE NAME':<20} | {'EXPECTED':<8} | {'SCORE':<6} | {'VERDICT':<15} | {'RESULT'}")
    print("-" * 70)
    
    passes = 0
    for r in results:
        status = "PASS" if r["success"] else "FAIL"
        if r["success"]: passes += 1
        print(f"{r['name']:<20} | {r['expected']:<8} | {r['score']:.3f} | {r['verdict']:<15} | {status}")
    
    print("-" * 70)
    accuracy = (passes / len(results)) * 100
    print(f"OVERALL ACCURACY: {accuracy:.1f}% ({passes}/{len(results)})")
    print("="*70 + "\n")

    # Reasoning check for first sample
    first = results[0]
    print(f"Forensic Reasoning Sample ({first['name']}):")
    print(f"  {first['reasoning'][:200]}...")
    print("\n[VALIDATION COMPLETE]")

if __name__ == "__main__":
    run_validation()
