import sys
import os

# Add parent dir to path
sys.path.append(os.getcwd())

from app.models.new_forensic_engine import analyze_forensic, load_models

def debug_technical():
    load_models()
    # Text from user's screenshot about Transformers
    text = """
    Transformers are a type of deep learning architecture that completely changed how machines process sequential data like text, audio, and even images. They were introduced in the 2017 research paper 'Attention Is All You Need' and are now the backbone of most modern AI systems, including models like ChatGPT. At a high level, transformers are designed to understand relationships between different parts of input data—especially long sequences—much more efficiently than older models like RNNs or LSTMs. Instead of processing data step-by-step (which is slow and limits memory), transformers process the entire sequence at once. This parallel processing is one of the main reasons they are faster and more scalable. The core idea behind transformers is something called self-attention.
    """
    
    print("\n--- DEBUGGING VANGUARD ON TECHNICAL PROSE ---")
    res = analyze_forensic(text)
    
    print(f"Verdict: {res['verdict']}")
    print(f"Score:   {res['score']}")
    print(f"Signals: {res['detailed_scores']}")
    print(f"Reasoning: {res['reasoning']}")

if __name__ == "__main__":
    debug_technical()
