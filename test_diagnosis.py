import sys
import os
from pathlib import Path

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), "backend"))

# Manually point to models for THIS test
ROOT = os.getcwd()
MODEL_PATH = os.path.join(ROOT, "onnx_models", "roberta").replace("\\", "/")

print(f"Checking model path: {MODEL_PATH}")
if not os.path.exists(MODEL_PATH):
    print("ERROR: Model path does not exist!")
    sys.exit(1)

# Import the logic, but we'll override the global models
from app.models import text_detector
from optimum.onnxruntime import ORTModelForSequenceClassification
from transformers import AutoTokenizer

print("Manually loading RoBERTa for diagnosis...")
text_detector.ROBERTA_MODEL = ORTModelForSequenceClassification.from_pretrained(
    MODEL_PATH, 
    file_name="model.onnx",
    local_files_only=True
)
text_detector.ROBERTA_TOK = AutoTokenizer.from_pretrained(MODEL_PATH, local_files_only=True)
print("RoBERTa loaded  ✓")

# The text that originally gave 74%
text = """Machine Learning is a subfield of Artificial Intelligence that focuses on enabling computers to learn from data and improve their performance without being explicitly programmed. Instead of relying on fixed rules, machine learning systems adapt by identifying patterns and making decisions based on past experiences. This makes them highly flexible and capable of handling complex tasks.

The main idea behind Machine Learning is to allow machines to learn automatically from data. By analyzing large datasets, algorithms can recognize trends and relationships that may not be obvious to humans. This ability to learn from data is what makes machine learning so powerful in solving real-world problems.

There are three primary types of Machine Learning: supervised learning, unsupervised learning, and reinforcement learning. In supervised learning, the model is trained using labeled data, meaning the correct answers are already known. This method is commonly used for tasks like classification and prediction.

Unsupervised learning, on the other hand, deals with unlabeled data. The system tries to find hidden patterns or groupings within the data without any prior knowledge of the outcomes. This approach is often used for clustering and data exploration.

Reinforcement learning is another important type, where an agent learns by interacting with its environment. It receives rewards or penalties based on its actions and gradually improves its strategy to achieve the best possible outcome. This method is widely used in robotics and gaming.

Machine Learning relies on algorithms and models to process data and make predictions. These models are trained using historical data and then tested on new data to evaluate their performance. The more high-quality data they receive, the better their predictions become.

One of the key advantages of Machine Learning is its ability to automate tasks that would otherwise require human intelligence. It can process large volumes of data quickly and accurately, making it useful in fields like finance, healthcare, and marketing.

Machine Learning is used in many everyday applications. For instance, recommendation systems on platforms like YouTube and Amazon suggest products or videos based on user behavior. It is also used in spam filtering, fraud detection, and speech recognition systems.

Despite its benefits, Machine Learning also has challenges. It requires large amounts of data, computational power, and careful model design. There is also the risk of bias in data, which can lead to inaccurate or unfair results if not handled properly.

In conclusion, Machine Learning is a rapidly growing field that is transforming the way technology works. As advancements continue, it will become even more integrated into daily life, helping to create smarter systems and more efficient solutions across various industries.
"""

# Run individual signals
s1 = text_detector.sig_roberta(text)
s2 = text_detector.sig_perplexity(text)
s3 = text_detector.sig_burstiness(text)
s4 = text_detector.sig_fast_detectgpt(text)
s5 = text_detector.sig_stylometric(text)

print(f"\n" + "="*40)
print(" FAKESHIELD DIAGNOSIS REPORT ")
print("="*40)

print(f"\nSignal breakdown:")
print(f"  S1 RoBERTa (ONNX):  {round(s1*100,1)}%  (Primary classifier)")
print(f"  S2 Perplexity:      {round(s2*100,1)}%  (Predictability)")
print(f"  S3 Burstiness:      {round(s3*100,1)}%  (Variation)")
print(f"  S4 Fast-DetectGPT:  {round(s4*100,1)}%  (Log-prob analysis)")
print(f"  S5 Stylometric:     {round(s5*100,1)}%  (AI Phrases/TTR)")

# v3.0 Production Weights
fused_raw = (
    0.55 * s1 +   # RoBERTa
    0.20 * s2 +   # Perplexity (gpt2-medium)
    0.10 * s3 +   # Burstiness
    0.10 * s4 +   # Fast-DetectGPT (hybrid + gpt2-medium)
    0.05 * s5     # Stylometric
)

# v3.0 Floor Logic
if s1 >= 0.85:
    current = max(fused_raw, s1 * 0.95)
elif s1 >= 0.70:
    current = max(fused_raw, s1 - 0.12)
else:
    current = fused_raw

print(f"\nCurrent fused score (v3.0): {round(current*100,1)}% ({'AI' if current >= 0.7 else 'LIKELY AI' if current >= 0.5 else 'HUMAN'})")

# Compare with original weights (0.40/0.25/0.15/0.12/0.08)
old = 0.40*s1 + 0.25*s2 + 0.15*s3 + 0.12*s4 + 0.08*s5
print(f"Original weights score:   {round(old*100,1)}%")

print("\n" + "="*40)
print(" CONCLUSION ")
print("="*40)
if s1 > 0.8 and current < 0.8:
    print("Diagnosis: RoBERTa is confident, but weaker signals (S2-S5) are dragging the score down.")
    print("Action: Increase RoBERTa's weight to 0.55 in app/models/text_detector.py.")
elif s1 < 0.8:
    print("Diagnosis: Even the primary classifier (RoBERTa) is uncertain about this modern AI text.")
    print("Action: Consider using a newer model or adding specific calibrators for GPT-4/Claude.")
else:
    print("Diagnosis: Signals are mostly in agreement.")
