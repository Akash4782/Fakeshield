import sys, os, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.models.new_forensic_engine import analyze_forensic, load_models

HUMAN_TEXT = """The dominant sequence transduction models are based on complex recurrent or convolutional neural networks in an encoder-decoder configuration. The best performing models also connect the encoder and decoder through an attention mechanism. We propose a new simple network architecture, the Transformer, based solely on attention mechanisms, dispensing with recurrence and convolutions entirely. Experiments on two machine translation tasks show these models to be superior in quality while being more parallelizable and requiring significantly less time to train. Our model achieves 28.4 BLEU on the WMT 2014 English-to-German translation task, improving over the existing best results, including ensembles by over 2 BLEU. On the WMT 2014 English-to-French translation task, our model establishes a new single-model state-of-the-art BLEU score of 41.8 after training for 3.5 days on eight GPUs, a small fraction of the training costs of the best models from the literature. We show that the Transformer generalizes well to other tasks by applying it successfully to English constituency parsing both with large and limited training data."""

AI_TEXT = """Deep learning is a specialized subset of machine learning that uses **artificial neural networks with many layers** (that’s where “deep” comes from) to learn complex patterns in data. It sits inside Machine Learning, which itself is part of Artificial Intelligence. The key idea is simple but powerful: instead of manually designing features from data, deep learning models automatically discover the most useful representations by stacking multiple processing layers.

Think of it like this—traditional machine learning often requires humans to tell the model what features matter (for example, edges in an image or keywords in text). Deep learning skips that manual step. A deep neural network learns low-level features in early layers (like edges or basic sounds), then combines them into higher-level features (like shapes, objects, or meanings) in deeper layers. This layered learning is what makes deep learning so effective for complex tasks like image recognition and language understanding.

At the core of deep learning are **neural networks**, which are loosely inspired by the human brain. A neural network consists of layers of nodes (neurons), where each neuron takes input, applies a mathematical transformation, and passes the result forward. During training, the network adjusts millions (sometimes billions) of parameters using techniques like backpropagation and optimization algorithms such as gradient descent. If that sounds heavy, it is—and that’s exactly why deep learning demands significant computational power, often using GPUs or specialized hardware.

There are several important types of deep learning architectures, and you should know what they’re actually used for instead of memorizing names blindly. Convolutional Neural Networks (CNNs) are designed for image-related tasks like object detection and face recognition. Recurrent Neural Networks (RNNs), and their improved versions like LSTMs, are used for sequential data such as text or time series. More recently, Transformer-based models have taken over tasks in natural language processing and even vision—these are the backbone behind systems like ChatGPT.

Deep learning has powered major breakthroughs in areas like speech recognition, medical imaging, self-driving cars, and recommendation systems. But here’s the reality most beginners ignore: deep learning is not a silver bullet. It needs **huge amounts of data**, careful tuning, and can easily overfit or behave like a black box. If you don’t understand what your model is learning, you can end up with results that look accurate but fail badly in real-world situations.

If you’re serious about learning this, don’t just jump into fancy frameworks like TensorFlow or PyTorch and copy tutorials. First understand how a single neuron works, how gradients update weights, and why deeper layers help. Otherwise, you’ll be stacking layers blindly without knowing why—and that’s exactly how people waste months without real progress.
"""

def test_samples():
    print("Initializing FakeShield v16.5 Elite Engine...")
    load_models()
    
    print("\n" + "="*50)
    print("TESTING HUMAN SAMPLE (Transformer Abstract)")
    print("="*50)
    t1 = time.time()
    res_human = analyze_forensic(HUMAN_TEXT, mode="deep")
    print(f"Verdict: {res_human.get('verdict')}")
    print(f"Score: {res_human.get('score')}")
    print(f"Signals: {res_human.get('signals')}")
    print(f"Reasoning: {res_human.get('forensic_reasoning')}")
    print(f"Time: {time.time()-t1:.2f}s")

    print("\n" + "="*50)
    print("TESTING AI SAMPLE (Deep Learning Explanation)")
    print("="*50)
    t2 = time.time()
    res_ai = analyze_forensic(AI_TEXT, mode="deep")
    print(f"Verdict: {res_ai.get('verdict')}")
    print(f"Score: {res_ai.get('score')}")
    print(f"Signals: {res_ai.get('signals')}")
    print(f"Reasoning: {res_ai.get('forensic_reasoning')}")
    print(f"Time: {time.time()-t2:.2f}s")

if __name__ == "__main__":
    test_samples()
