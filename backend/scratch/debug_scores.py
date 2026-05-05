import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.models.new_forensic_engine import analyze_forensic as analyze

ai_text = """Artificial intelligence (AI) refers to the simulation of human intelligence processes by machines, especially computer systems. These processes include learning (the acquisition of information and rules for using the information), reasoning (using rules to reach approximate or definite conclusions) and self-correction. Particular applications of AI include expert systems, speech recognition and machine vision.
Machine learning is a subset of AI that focuses on the use of data and algorithms to imitate the way that humans learn, gradually improving its accuracy. In conclusion, it is worth noting that deep learning is a specialized branch of machine learning that focuses on training neural networks. These models automatically learn features from raw data, making them highly effective across various industries.
Furthermore, the rapid evolution of large language models has transformed the landscape of natural language processing. By leveraging transformer architectures and massive datasets, these models can generate human-like text with remarkable fluency. This capability has significant implications for content creation, customer service, and research. However, it also raises important questions regarding the authenticity of digital content. As we move forward into 2026, the need for robust forensic detection tools becomes increasingly paramount to maintain the integrity of our information ecosystems and ensure trust in AI systems."""

result = analyze(ai_text, mode="deep")
print(f"SCORE: {result['score']}")
print(f"VERDICT: {result['verdict']}")
for k, v in result['signals'].items():
    print(f"  {k}: {v}")
