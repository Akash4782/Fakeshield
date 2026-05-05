import sys, os, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.models.text_classifier_ensemble import ensemble_predict

human = "Deep learning, the subset of machine learning driven by large artificial neural networks, has emerged over the past few decades as the state-of-the-art AI model architecture across nearly every domain in which AI is used. In contrast to the explicitly defined algorithms of traditional machine learning, deep learning relies on distributed networks of mathematical operations that provide an unparalleled ability to learn the intricate nuances of very complex data."

ai = "Certainly! Here is a quick overview of machine learning. Machine learning is a fascinating branch of artificial intelligence. At its core, it is about teaching computers to learn from data. Think of it like this: instead of writing explicit rules for the computer to follow, you feed it a massive dataset and let it find the patterns. It is truly a paradigm shift in how we approach problem solving. In conclusion, the possibilities are endless."

res_human = ensemble_predict(human, mode='deep')
res_ai = ensemble_predict(ai, mode='deep')

print("\n--- HUMAN TEXT ---")
print(res_human['layer_scores'])
print(f"Final: {res_human['ai_probability']}")

print("\n--- AI TEXT ---")
print(res_ai['layer_scores'])
print(f"Final: {res_ai['ai_probability']}")
