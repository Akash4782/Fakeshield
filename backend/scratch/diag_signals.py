import sys, os
sys.path.insert(0, '.')
os.environ['PYTHONUTF8'] = '1'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION'] = 'python'

# Typical AI-generated ML explanation text
ai_text = (
    "Machine learning is a subset of artificial intelligence that enables systems to learn and improve "
    "from experience without being explicitly programmed. It focuses on developing computer programs that "
    "can access data and use it to learn for themselves. The process begins with observations or data, such "
    "as examples, direct experience, or instruction, so that computers can learn to make better decisions "
    "based on the patterns they find in the data. The primary aim is to allow computers to learn automatically "
    "without human intervention or assistance and adjust actions accordingly. There are three main types of "
    "machine learning: supervised learning, unsupervised learning, and reinforcement learning. Supervised "
    "learning involves training a model on labeled data, where the correct answers are provided. Unsupervised "
    "learning deals with unlabeled data, and the model tries to find hidden patterns or intrinsic structures "
    "in the input. Reinforcement learning is based on rewarding desired behaviors and punishing undesired ones."
)

from app.models.structural_engine import StructuralEngine
from app.models.semantic_drift import SemanticDriftEngine

se = StructuralEngine()
sd = SemanticDriftEngine()

struct = se.analyze(ai_text)
drift = sd.analyze(ai_text)

print("=== STRUCTURAL ===")
print("  structural_strength:", struct["structural_strength"])
print("  high_uniformity:    ", struct["high_uniformity"])
print("  structural_variation:", struct["structural_variation"])
print("  details:", struct["details"])

print()
print("=== SEMANTIC ===")
print("  semantic_irregularity:", drift["semantic_irregularity"])
print("  semantic_uniformity:  ", drift["semantic_uniformity"])
print("  details:", drift["details"])
