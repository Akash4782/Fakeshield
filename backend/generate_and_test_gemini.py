import os
import sys
import google.generativeai as genai
from app.config import settings
from app.models.new_forensic_engine import analyze_forensic as analyze

# Initialize Gemini for generation
api_key = settings.GEMINI_API_KEY
if not api_key:
    print("Error: No GEMINI_API_KEY found.")
    sys.exit(1)

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-3.1-flash-lite-preview")

topics = [
    "The future of quantum computing and its impact on cybersecurity.",
    "Explain the importance of biodiversity in rain forests.",
    "How does a transformer neural network work?"
]

print("--- GENERATING GEMINI TEXT SAMPLES ---")
samples = []
for topic in topics:
    print(f"Generating for topic: {topic}")
    prompt = f"Write a detailed 3-paragraph explanation about: {topic}. Use a helpful, informative, and neutral tone."
    response = model.generate_content(prompt)
    samples.append(response.text)

print("\n--- TESTING FORENSIC ENGINE ON GENERATED GEMINI TEXT ---")
for i, text in enumerate(samples):
    print(f"\nSample {i+1} (Topic: {topics[i]}):")
    print("-" * 30)
    print(text[:100] + "...")
    print("-" * 30)
    
    result = analyze(text, mode="deep")
    
    print(f"Verdict: {result['verdict']} ({round(result['score']*100, 1)}%)")
    print("Signals:")
    for k, v in result['signals'].items():
        print(f"  {k}: {round(v*100, 1)}%")
    
    print(f"Modern Fingerprint: {result['signals'].get('modern_fingerprint', 0)}")
    print(f"Forensic Reasoning: {result.get('forensic_reasoning', 'N/A')[:200]}...")
    print("=" * 50)
