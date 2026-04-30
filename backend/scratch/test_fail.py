import sys
import os
sys.path.append(os.getcwd())

from app.models.new_forensic_engine import analyze_forensic
import json

test_text = """You are a top 0.1% AI researcher, startup architect, and NLP expert specializing in LLM evaluation and AI-generated content detection.

Your task is NOT to give generic advice.
Your task is to DESIGN a STARTUP-LEVEL AI TEXT DETECTION SYSTEM using ONLY PRETRAINED MODELS.

Context:
I am building an "AI Text Lab" that classifies:
- AI-generated text
- Human-written text

Current problem:
- My system is inaccurate
- Fails on real-world inputs
- Not reliable for production use

Constraints:
- NO model training allowed
- ONLY pretrained models, APIs, and inference-based techniques
- Must be hackathon-ready AND scalable to startup level

Goal:
- High real-world accuracy
- Strong visual demo
- Startup-grade architecture
- Explainable outputs (very important)"""

print("--- STARTING DETAILED FORENSIC DEBUG ---")
results = analyze_forensic(test_text)
print(json.dumps(results, indent=2))
