import os
import time
import json
import google.generativeai as genai
from app.config import settings

def generate_samples():
    if not settings.GEMINI_API_KEY:
        print("Error: GEMINI_API_KEY not found.")
        return

    genai.configure(api_key=settings.GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')

    dataset = {"human": [], "ai": []}

    # 1. Generate 40 Human Samples (Simulated Human Authorship)
    # Categories: Academic, Blog, News, Wikipedia
    human_categories = [
        "A formal academic introduction to a research paper on quantum computing with citations.",
        "A personal blog post about learning to cook Italian food in Rome.",
        "A factual Wikipedia-style biography of a 19th-century explorer.",
        "A nuanced news report about a local election with quotes from residents.",
        "A technical deep-dive into the Linux kernel memory management.",
        "A creative short story about a clockmaker in a steampunk world.",
        "A scientific abstract about the discovery of a new exoplanet.",
        "A legal analysis of privacy laws in the digital age.",
        "A philosophical essay on the nature of consciousness.",
        "A travel guide for a remote village in the Himalayas."
    ]

    print("Generating 40 Human samples (Simulating real-world human data)...")
    for cat in human_categories:
        for i in range(4): # 10 cats * 4 = 40 samples
            prompt = f"Write a {cat} (approx 250-300 words). Ensure the style is organic, with varying sentence lengths, occasional minor imperfections, and complex rhetorical structures typical of human authors. Do NOT make it sound like a generic AI response."
            try:
                response = model.generate_content(prompt)
                dataset["human"].append(response.text.strip())
                print(f"  Generated Human Sample {len(dataset['human'])}/40")
                time.sleep(1) # Rate limit protection
            except Exception as e:
                print(f"Error generating human sample: {e}")

    # 2. Generate 40 AI Samples
    # Categories: GPT-4 style, GPT-3.5 style, Claude style, Gemini style
    ai_categories = [
        "Write a structured essay on 'The Future of AI' (GPT-4 style, very polished).",
        "Write a generic explanation of photosynthesis (GPT-3.5 style, list-heavy).",
        "Explain how a mortgage works (Claude style, empathetic and clear).",
        "Summarize the history of the internet (Gemini style, concise and technical).",
        "Write a blog post about 'Sustainable Living' (Generic AI style).",
        "Describe the benefits of remote work (Typical structured AI response).",
        "Explain the theory of relativity (AI tutor style).",
        "Write a cover letter for a software engineer (AI assistant style).",
        "Discuss the pros and cons of nuclear energy (Neutral AI balance).",
        "Write a recipe for sourdough bread with an AI introduction."
    ]

    print("\nGenerating 40 AI samples...")
    for cat in ai_categories:
        for i in range(4): # 10 cats * 4 = 40 samples
            prompt = f"{cat} (approx 250-300 words). Use typical AI structures like numbered lists, clear transitions (e.g., 'In conclusion', 'Furthermore'), and consistent sentence rhythms."
            try:
                response = model.generate_content(prompt)
                dataset["ai"].append(response.text.strip())
                print(f"  Generated AI Sample {len(dataset['ai'])}/40")
                time.sleep(1)
            except Exception as e:
                print(f"Error generating AI sample: {e}")

    # Save to file
    with open("benchmark_80_samples.json", "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=2)
    print("\nSUCCESS: Dataset saved to benchmark_80_samples.json")

if __name__ == "__main__":
    generate_samples()
