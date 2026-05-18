import os
import sys

# Set env to avoid problems
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

# Add backend dir to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.models.text_classifier_ensemble import ensemble_predict

human_text = """The rapid development of machine learning has brought significant changes to various industries. Researchers are continuously exploring new architectures to improve efficiency. I believe that in the next few years, we will see even more incredible advancements. It's truly fascinating to see how fast everything is moving!"""

human_text2 = """The quick brown fox jumps over the lazy dog. Yesterday I was walking down the street when I saw a beautiful red car speeding by. I wondered where it was going so fast, maybe there was an emergency? Who knows. Anyway, I bought some milk at the grocery store and went home. The weather was quite chilly, so I made myself a cup of hot chocolate and watched a movie. It was a really relaxing evening after a long and exhausting day at work. I hope tomorrow brings better news."""

ai_text = """As an AI language model, I can tell you that artificial intelligence is a rapidly growing field with many exciting applications in everyday life. We can see its impact across numerous sectors, such as healthcare, finance, and transportation. Furthermore, natural language processing models like ChatGPT can generate text that is highly coherent and human-like. This technology has revolutionized the way we interact with machines and has the potential to solve complex problems in various domains."""

ai_text2 = """Artificial Intelligence (AI) refers to the simulation of human intelligence in machines that are programmed to think like humans and mimic their actions. The term may also be applied to any machine that exhibits traits associated with a human mind such as learning and problem-solving. The ideal characteristic of artificial intelligence is its ability to rationalize and take actions that have the best chance of achieving a specific goal."""

print("Testing HUMAN TEXT 1:")
res = ensemble_predict(human_text)
print(f"Verdict: {res.get('verdict')}, Score: {res.get('score')}")
print(f"Signals: {res.get('signals')}\n")

print("Testing HUMAN TEXT 2:")
res = ensemble_predict(human_text2)
print(f"Verdict: {res.get('verdict')}, Score: {res.get('score')}")
print(f"Signals: {res.get('signals')}\n")

print("Testing AI TEXT 1:")
res = ensemble_predict(ai_text)
print(f"Verdict: {res.get('verdict')}, Score: {res.get('score')}")
print(f"Signals: {res.get('signals')}\n")

print("Testing AI TEXT 2:")
res = ensemble_predict(ai_text2)
print(f"Verdict: {res.get('verdict')}, Score: {res.get('score')}")
print(f"Signals: {res.get('signals')}\n")
