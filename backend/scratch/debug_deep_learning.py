import sys, os, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.models.text_classifier_ensemble import (
    ensemble_predict, load_neural_detector, load_ppl_engine,
    load_bino_engine, load_modern_llm_detector, _ai_lexical_score,
    _human_style_bias, _burstiness, _ppl_to_ai_prob, _compute_ppl,
    _multi_model_neural_vote, _models
)

text = """Deep learning is a specialized subset of machine learning that uses **artificial neural networks with many layers** (that's where "deep" comes from) to learn complex patterns in data. It sits inside Machine Learning, which itself is part of Artificial Intelligence. The key idea is simple but powerful: instead of manually designing features from data, deep learning models automatically discover the most useful representations by stacking multiple processing layers.

Think of it like this—traditional machine learning often requires humans to tell the model what features matter (for example, edges in an image or keywords in text). Deep learning skips that manual step. A deep neural network learns low-level features in early layers (like edges or basic sounds), then combines them into higher-level features (like shapes, objects, or meanings) in deeper layers. This layered learning is what makes deep learning so effective for complex tasks like image recognition and language understanding.

At the core of deep learning are **neural networks**, which are loosely inspired by the human brain. A neural network consists of layers of nodes (neurons), where each neuron takes input, applies a mathematical transformation, and passes the result forward. During training, the network adjusts millions (sometimes billions) of parameters using techniques like backpropagation and optimization algorithms such as gradient descent. If that sounds heavy, it is—and that's exactly why deep learning demands significant computational power, often using GPUs or specialized hardware.

There are several important types of deep learning architectures, and you should know what they're actually used for instead of memorizing names blindly. Convolutional Neural Networks (CNNs) are designed for image-related tasks like object detection and face recognition. Recurrent Neural Networks (RNNs), and their improved versions like LSTMs, are used for sequential data such as text or time series. More recently, Transformer-based models have taken over tasks in natural language processing and even vision—these are the backbone behind systems like ChatGPT.

Deep learning has powered major breakthroughs in areas like speech recognition, medical imaging, self-driving cars, and recommendation systems. But here's the reality most beginners ignore: deep learning is not a silver bullet. It needs **huge amounts of data**, careful tuning, and can easily overfit or behave like a black box. If you don't understand what your model is learning, you can end up with results that look accurate but fail badly in real-world situations.

If you're serious about learning this, don't just jump into fancy frameworks like TensorFlow or PyTorch and copy tutorials. First understand how a single neuron works, how gradients update weights, and why deeper layers help. Otherwise, you'll be stacking layers blindly without knowing why—and that's exactly how people waste months without real progress."""

print("Loading models...")
load_neural_detector()
load_ppl_engine()
load_bino_engine()
load_modern_llm_detector()
print("Models loaded.\n")

# --- Individual signal debug ---
print("=== INDIVIDUAL SIGNAL ANALYSIS ===")
print(f"Neural models loaded: {list(_models.keys())}")

neural = _multi_model_neural_vote(text)
print(f"\nNeural Vote:")
print(f"  Weighted avg  : {neural['avg_score']:.4f}")
for name, score in neural.get('per_model', {}).items():
    print(f"  [{name}]      : {score:.4f}")

ppl_val = _compute_ppl(text)
ppl_ai = _ppl_to_ai_prob(ppl_val)
print(f"\nPPL Engine:")
print(f"  Raw PPL       : {ppl_val:.2f}")
print(f"  PPL → AI Prob : {ppl_ai:.4f}")

burst = _burstiness(text)
print(f"\nBurstiness (low=AI): {burst:.4f}")

lex = _ai_lexical_score(text)
print(f"Lexical AI phrases: {lex:.4f}")

human_bias = _human_style_bias(text)
print(f"Human Shield bias : {human_bias:.4f}")

print("\n=== FULL ENSEMBLE RESULT ===")
res = ensemble_predict(text, mode="deep")
print(f"Final AI Prob : {res['ai_probability']:.4f} ({res['ai_probability']*100:.1f}%)")
print(f"Verdict       : {res['verdict']}")
print(f"Layer Scores  : {res['layer_scores']}")
