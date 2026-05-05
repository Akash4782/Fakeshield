import json
from app.models.new_forensic_engine import analyze_forensic

ai_text = """Machine learning is a branch of Artificial Intelligence that focuses on building systems that can learn patterns from data and improve their performance over time without being explicitly programmed for every task. Instead of writing rigid rules (like traditional programming), you feed the system data, and it automatically discovers relationships, trends, and structures within that data. This makes machine learning especially powerful for problems where writing rules manually would be too complex or impossible—such as recognizing speech, detecting fraud, or predicting user behavior.

At its core, machine learning works by training a model. A model is a mathematical function that takes input data and produces an output. During training, the model is shown large amounts of data and adjusts its internal parameters to minimize errors in its predictions. For example, if you want a model to recognize cats in images, you train it on thousands of labeled images (cats vs. non-cats). Over time, the model learns what visual patterns (like shapes, textures, edges) are associated with cats.

There are three main types of machine learning. The first is supervised learning, where the model is trained on labeled data—meaning the correct output is already known. This is used for tasks like classification (spam vs. not spam) and regression (predicting house prices). The second is unsupervised learning, where the data has no labels, and the model tries to find hidden patterns or groupings on its own, such as clustering customers based on behavior. The third is reinforcement learning, where an agent learns by interacting with an environment and receiving rewards or penalties, commonly used in robotics and game-playing systems.

Machine learning models rely heavily on data quality and quantity. If the data is biased, incomplete, or noisy, the model will learn incorrect patterns and produce poor results—this is known as “garbage in, garbage out.” Additionally, models must be evaluated properly using unseen data to ensure they generalize well and are not just memorizing the training data (a problem called overfitting). This is why techniques like cross-validation, regularization, and proper dataset splitting are critical in real-world applications.

In modern applications, machine learning powers many systems you use daily—recommendation engines on platforms like YouTube, voice assistants, autonomous vehicles, and medical diagnosis tools. A more advanced subset of machine learning is Deep Learning, which uses neural networks with many layers to model highly complex patterns, especially in images, audio, and text.

Here’s the reality check: machine learning is not magic. It doesn’t “understand” things the way humans do—it just finds statistical patterns. If you’re planning to build serious projects or a career in it, you need strong fundamentals in mathematics (especially linear algebra, probability, and calculus), programming (usually Python), and data handling. People who skip these basics and jump straight to using APIs or pre-trained models end up stuck when things don’t work. If you want to actually be good, you need to understand what’s happening under the hood, not just copy code from tutorials."""

human_text = """As a scientific endeavour, machine learning grew out of the quest for artificial intelligence (AI). In the early days of AI as an academic discipline, some researchers were interested in having machines learn from data. They attempted to approach the problem with various symbolic methods, as well as what were then termed "neural networks"; these were mostly perceptrons and other models that were later found to be reinventions of the generalised linear models of statistics.[21] Probabilistic reasoning was also employed, especially in automated medical diagnosis.[22]: 488 

However, an increasing emphasis on the logical, knowledge-based approach caused a rift between AI and machine learning. Probabilistic systems were plagued by theoretical and practical problems of data acquisition and representation.[22]: 488  By 1980, expert systems had come to dominate AI, and statistics was out of favour.[23] Work on symbolic/knowledge-based learning continued within AI, leading to inductive logic programming (ILP), but the more statistical line of research was now outside the field of AI proper, in pattern recognition and information retrieval.[22]: 708–710, 755  Neural network research was abandoned by AI and computer science around the same time. This subfield, termed "connectionism", was continued by researchers from other disciplines, including John Hopfield, David Rumelhart, and Geoffrey Hinton. Their main success came in the mid-1980s with the reinvention of backpropagation.[22]: 25 

Machine learning (ML), reorganised and recognised as its own field, started to flourish in the 1990s. The field changed its goal from achieving artificial intelligence to tackling solvable problems of a practical nature. It shifted focus away from the symbolic approaches it had inherited from AI, and toward methods and models borrowed from statistics, fuzzy logic, and probability theory.[23]"""

print("--- ANALYZING AI TEXT ---")
res_ai = analyze_forensic(ai_text, mode='deep')
print(json.dumps(res_ai, indent=2))

print("\n--- ANALYZING HUMAN TEXT ---")
res_human = analyze_forensic(human_text, mode='deep')
print(json.dumps(res_human, indent=2))
