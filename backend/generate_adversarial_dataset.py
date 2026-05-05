import json
import os
import time
import google.generativeai as genai
from typing import List, Dict
import random

# Configuration
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
MODEL_NAME = "gemini-2.0-flash"
OUTPUT_FILE = "vanguard_adversarial_dataset.json"
TARGET_SAMPLES = 80 # 40 Human, 40 AI

TOPICS = [
    "Quantum Physics & Entanglement", "Existential Philosophy", "Paleoanthropology", 
    "Music Theory & Wagner", "Brutalist Architecture", "Neuroscience of Qualia",
    "Global Culinary History", "Maritime International Law", "Generative Linguistics",
    "Cosmological Holography", "Urban Sociology", "Ecological Modernism",
    "Political Resource Curse", "Film Noir Aesthetics", "Virtual Reality Mechanics",
    "Critical Theory & Post-modernism", "Zero Trust Cybersecurity", "Edge AI Latency",
    "Multi-cloud Governance", "Blockchain & NFTs", "5G Network Slicing",
    "Autonomous Vehicle Sensors", "IoT Smart Home Security", "Big Data Pipelines",
    "E-commerce Personalization"
]

def generate_sample(topic: str, label: str) -> str:
    """Generates a high-quality long-form sample using Gemini."""
    if not GEMINI_API_KEY:
        print("Error: GEMINI_API_KEY not found.")
        return ""

    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel(MODEL_NAME)

    if label == "HUMAN":
        prompt = f"""
        Act as a highly experienced academic or a niche professional.
        Write a deep-dive analysis on the topic: '{topic}'.
        
        CRITICAL STYLE GUIDELINES (HUMAN):
        - Use complex, non-linear sentence structures.
        - Include specific historical dates, minor technical glitches in reasoning, or highly personal anecdotes.
        - Use colloquial but professional phrasing.
        - Avoid the 'AI structure' (Introduction, Point 1, Point 2, Conclusion).
        - The text MUST be between 250 and 400 words.
        - DO NOT include any AI-typical transitions like 'Furthermore' or 'In conclusion'.
        """
    else:
        prompt = f"""
        Act as a state-of-the-art AI assistant (GPT-4/Claude style).
        Write a detailed technical overview on the topic: '{topic}'.
        
        CRITICAL STYLE GUIDELINES (AI):
        - Use clean, logical hierarchies.
        - Use transitions like 'Furthermore', 'Moreover', and 'In summary'.
        - Maintain a neutral, balanced, and authoritative tone.
        - The text MUST be between 250 and 400 words.
        - Ensure a very high standard of grammatical perfection and 'over-smooth' transitions.
        """

    try:
        response = model.generate_content(prompt)
        text = response.text.strip()
        # Basic cleanup
        text = text.replace("```", "").replace("---", "").strip()
        return text
    except Exception as e:
        print(f"Error generating {label} sample for {topic}: {e}")
        return ""

def main():
    print(f"--- Vanguard Forensic Dataset Generator (80 Samples) ---")
    
    samples = []
    
    # Generate 40 Human Samples
    print(f"\n[PHASE 1] Generating 40 Human Samples...")
    for i in range(40):
        topic = random.choice(TOPICS)
        print(f"  ({i+1}/40) Human: {topic}...", end="", flush=True)
        text = generate_sample(topic, "HUMAN")
        if text:
            samples.append({"text": text, "label": "HUMAN", "topic": topic})
            print(" DONE")
        else:
            print(" FAILED")
        time.sleep(2) # Avoid rate limits

    # Generate 40 AI Samples
    print(f"\n[PHASE 2] Generating 40 AI Samples...")
    for i in range(40):
        topic = random.choice(TOPICS)
        print(f"  ({i+1}/40) AI: {topic}...", end="", flush=True)
        text = generate_sample(topic, "AI")
        if text:
            samples.append({"text": text, "label": "AI", "topic": topic})
            print(" DONE")
        else:
            print(" FAILED")
        time.sleep(2)

    # Save
    dataset = {"samples": samples}
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(dataset, f, indent=2)
    
    print(f"\n[SUCCESS] Generated {len(samples)} samples to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
