import sys, os, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.models.text_classifier_ensemble import ensemble_predict

text = """Machine learning is the subset of artificial intelligence (AI) that focuses on algorithms that can "learn" the patterns of training data and subsequently, make accurate inferences about new data. This pattern recognition ability enables machine learning models to make decisions or predictions without explicit, hard-coded instructions. Machine learning has completely revolutionized the field of AI: it provides the backbone of most modern AI systems, from weather forecasting models to autonomous vehicles to large language models (LLMs) and other generative AI tools. The central premise of machine learning (ML) is that if you optimize a model's performance on a dataset of tasks that accurately resemble the real-world problems it will be used for—a process called model training—the model can make accurate predictions on the new data it sees in its ultimate use case. Training a model is a means to an end: generalization, the translation of training to real-world scenarios.

Rather, deep learning—artificial neural networks, specifically—has taken over the past few decades as the state-of-the-art AI architecture across nearly every domain in which AI is used. In contrast to the explicitly defined algorithms of classical machine learning, deep learning relies on distributed networks of mathematical operations that provide an unmatched ability to learn the intricate nuances of very complex data. Because deep learning requires very large amounts of data and compute to function effectively, its advent has coincided with the escalating availability of data and graphics processing units (GPUs). The discipline of machine learning is closely intertwined with that of data science. In a sense, machine learning can be viewed as a collection of algorithms and techniques to automate the extraction of insights and, importantly, apply learnings from data to automate the execution of relevant tasks. The origin of the term (and the core concept itself) is often attributed to Arthur L. Samuel's 1959 article in IBM Journal, "Some Studies in Machine Learning Using the Game of Checkers." """

print("\n=== RUNNING FULL ENSEMBLE ===")
res = ensemble_predict(text, mode="deep")
print(f"Final AI Prob : {res['ai_probability']:.4f} ({res['ai_probability']*100:.1f}%)")
print(f"Verdict       : {res['verdict']}")
print(f"Layer Scores  : {res['layer_scores']}")
print(f"Reasoning     : {res['reasoning']}")
