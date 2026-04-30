import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from app.models.new_forensic_engine import analyze_forensic as analyze

text = """The transformer model is a type of neural network architecture that excels at processing sequential data, most prominently associated with large language models (LLMs). Transformer models have also achieved elite performance in other fields of artificial intelligence (AI), such as computer vision, speech recognition and time series forecasting. The transformer architecture was first described in the seminal 2017 paper "Attention is All You Need" by Vaswani and others, which is now considered a watershed moment in deep learning. Originally introduced as an evolution of the recurrent neural network (RNN)-based sequence-to-sequence models used for machine translation, transformer-based models have since attained cutting-edge advancements across nearly every machine learning (ML) discipline. Despite their versatility, transformer models are still..."""

print("Testing Technical Human Text:")
print(text[:100] + "...\n")
result = analyze(text, mode="deep")

print("\n" + "="*50)
print(f"Verdict: {result['verdict']} ({round(result['score']*100, 1)}%)")
print("Signals:")
for k, v in result['signals'].items():
    print(f"  {k}: {round(v*100, 1)}%")

print(f"\nForensic Reasoning:\n{result.get('forensic_reasoning', 'N/A')}")

print("\nSentence Highlights:")
for h in result['sentence_highlights']:
    print(f"  [{h['label']}] ({h.get('ai_score', 'N/A')}%) {h['sentence'][:60]}...")
print("="*50 + "\n")
