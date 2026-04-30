import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from app.models.new_forensic_engine import analyze_forensic as analyze

# Standard ChatGPT-style explanation (High AI content)
ai_text = """Artificial intelligence (AI) refers to the simulation of human intelligence processes by machines, especially computer systems. These processes include learning (the acquisition of information and rules for using the information), reasoning (using rules to reach approximate or definite conclusions) and self-correction. Particular applications of AI include expert systems, speech recognition and machine vision.

Machine learning is a subset of AI that focuses on the use of data and algorithms to imitate the way that humans learn, gradually improving its accuracy. In conclusion, it is worth noting that deep learning is a specialized branch of machine learning that focuses on training neural networks. These models automatically learn features from raw data, making them highly effective across various industries."""

print("Testing AI text:")
print(ai_text[:100] + "...\n")
result = analyze(ai_text, mode="deep")

print("\n" + "="*50)
print(f"Verdict: {result['verdict']} ({round(result['score']*100, 1)}%)")
print("Signals:")
for k, v in result['signals'].items():
    print(f"  {k}: {round(v*100, 1)}%")
print("\nSentence Highlights:")
for h in result['sentence_highlights']:
    print(f"  [{h['label']}] ({h.get('ai_score', 'N/A')}%) {h['sentence'][:60]}...")
print("="*50 + "\n")

# Should still be > 80%
if result['score'] * 100 >= 80:
    print("SUCCESS: AI detection sensitivity maintained.")
else:
    print("WARNING: AI detection sensitivity might be too low.")
    sys.exit(1)
