
import sys
import os

# Add the backend directory to sys.path
sys.path.append(os.getcwd())

from app.models.text_classifier_ensemble import ensemble_predict
import json

HUMAN_TEXT_1 = """
Artificial intelligence (AI) is the intelligence of machines or software, as opposed to the intelligence of living beings, such as humans or other animals. It is a field of study in computer science that develops and studies intelligent machines. Such machines may be called AIs. AI technology is widely used throughout industry, government, and science. Some high-profile applications are: advanced web search engines (e.g., Google Search); recommendation systems (used by YouTube, Amazon, and Netflix); understanding human speech (such as Siri and Alexa); self-driving cars (e.g., Waymo); generative or creative tools (ChatGPT and AI art); and playing games and analysis in strategy games (such as chess and Go).
"""

AI_TEXT_1 = """
Quantum computing is a rapidly emerging technology that harnesses the laws of quantum mechanics to solve problems too complex for classical computers. Today, IBM Quantum makes real quantum hardware—a tool scientists only began to imagine three decades ago—available to hundreds of thousands of developers. Our engineers deliver ever-more-powerful superconducting quantum processors at regular intervals, on a path toward the quantum computing speed and capacity necessary to change the world. These machines are very different from the classical computers that have been around for more than half a century. Here’s a look at how this technology works.
"""

# Let's add a more "Academic/Human" text with citations and complex structure
HUMAN_TEXT_2 = """
The study of neural networks has historically been divided into two distinct epochs: the symbolic era and the connectionist resurgence (Rumelhart et al., 1986). While early pioneers sought to encode human logic via discrete propositional calculus, contemporary deep learning architectures—most notably the transformer (Vaswani et al., 2017)—operate on the principle of self-attention mechanisms. It is important to note that, despite their impressive performance on benchmarks like GLUE or SuperGLUE, these models often lack true semantic grounding. As noted by Bender and Koller (2020), an agent trained solely on form cannot learn meaning, a concept they illustrate with the 'octopus' thought experiment. This tension between statistical pattern matching and genuine understanding remains the central polemic of modern computational linguistics.
"""

# And a very "Machine-Perfect" AI text
AI_TEXT_2 = """
Deep learning is a subset of machine learning that is based on artificial neural networks with multiple layers. These networks are designed to simulate the way the human brain processes information. By using large datasets, deep learning models can automatically learn to recognize patterns and make decisions. This technology has revolutionized many fields, including computer vision, natural language processing, and speech recognition. One of the key advantages of deep learning is its ability to handle unstructured data, such as images and text, without the need for manual feature engineering. As we continue to develop more advanced algorithms and more powerful hardware, the potential applications of deep learning are virtually limitless.
"""

samples = [
    ("Human Wikipedia", HUMAN_TEXT_1),
    ("AI Explainer", AI_TEXT_1),
    ("Human Academic", HUMAN_TEXT_2),
    ("AI Generic", AI_TEXT_2)
]

print("--- FakeShield AI Text Lab Forensic Audit (v14.0) ---")

for name, text in samples:
    print(f"\n[TESTING: {name}]")
    result = ensemble_predict(text, mode="standard")
    
    print(f"Verdict: {result['verdict']} (Score: {result['ai_probability']})")
    print(f"Threat Level: {result['threat']}")
    print(f"Confidence: {result['confidence']}")
    print(f"Signals: {json.dumps(result['signals'], indent=2)}")
    print(f"Raw Metrics: {json.dumps(result.get('raw_metrics', {}), indent=2)}")
    print(f"Reasoning: {result['reasoning']}")
    
    # Check supplementary layers
    structural = result.get('structural_details', {})
    semantic = result.get('semantic_details', {})
    
    print(f"Structural Integrity: {structural.get('structural_strength', 'N/A')} (Uniformity: {structural.get('high_uniformity', 'N/A')})")
    print(f"Semantic Drift: {semantic.get('semantic_irregularity', 'N/A')} (Uniformity: {semantic.get('semantic_uniformity', 'N/A')})")
    print("-" * 50)
