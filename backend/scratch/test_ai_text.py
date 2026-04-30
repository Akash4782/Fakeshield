import sys
import os
import re
import numpy as np
sys.path.append(os.getcwd())

from app.models.text_classifier_ensemble import _academic_domain_bias, _ai_lexical_score

text = """Deep learning is a specialized subset of machine learning. It uses **artificial neural networks with many layers** (that's where the "deep" comes from) to learn complex patterns in data. Machine Learning, which itself is part of Artificial Intelligence. The key idea is simple but powerful: instead of manually designing features from data, deep learning models automatically discover the most useful representations by stacking multiple processing layers. Think of it like this: traditional machine learning often requires humans to tell the model what features matter (for example, edges in an image or keywords in text). Deep learning skips that manual step. A deep neural network learns low-level features in early layers (like edges or basic sounds), then combines them into higher-level features (like shapes, objects, or meanings) in deeper layers. This layered learning is what makes deep learning so effective for complex tasks like image recognition and language understanding. At the core of deep learning are **neural networks**, which are loosely inspired by the human brain."""

bias = _academic_domain_bias(text)
lex = _ai_lexical_score(text)

print(f"Text Length (words): {len(text.split())}")
print(f"Academic Bias: {bias}")
print(f"Lexical Score: {lex}")
