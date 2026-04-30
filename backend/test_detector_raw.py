import sys
sys.path.append('.')
from app.models.text_detector import (
    sig_roberta, sig_perplexity, sig_burstiness, sig_fast_detectgpt, sig_stylometric,
    _compute_gpt2_features, analyze
)

text = """Deep learning is a specialized branch of machine learning that focuses on training artificial neural networks with many layers (hence "deep") to learn patterns from large amounts of data. Inspired by the structure of the human brain, these neural networks consist of interconnected nodes (neurons) that process information and pass it forward. Deep learning models are particularly powerful because they can automatically learn features from raw data, reducing the need for manual feature engineering. 

At the core of deep learning are artificial neural networks, which are made up of input layers, hidden layers, and output layers. Each layer transforms the data using mathematical operations, allowing the network to gradually learn complex patterns. The more layers a network has, the more abstract and high-level features it can capture. For example, in image recognition, early layers may detect edges, while deeper layers recognize objects like faces or animals.

One of the most important aspects of deep learning is the training process."""

print("Computing GPT-2 features...")
cache = _compute_gpt2_features(text)
print("PPL:", cache["ppl"])
print("mean_lp:", cache["mean_lp"])
print("median_lp:", cache["median_lp"])
print("var_lp:", cache["var_lp"])
print("hc:", cache["hc"])
print("vhc:", cache["vhc"])

print("-" * 30)
print("s2 Perplexity:", sig_perplexity(text, cache))
print("s4 FastDetectGPT:", sig_fast_detectgpt(text, cache))
print("s3 Burstiness:", sig_burstiness(text))
print("s5 Stylometric:", sig_stylometric(text))
print("s1 Roberta:", sig_roberta(text))

print("-" * 30)
res = analyze(text, include_highlights=False, mode="deep")
print("Verdict:", res["verdict"], res["confidence"])
