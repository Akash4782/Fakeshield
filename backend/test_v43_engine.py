import sys
import os

# Add parent dir to path
sys.path.append(os.getcwd())

from app.models.new_forensic_engine import analyze_forensic, load_models

def test_v43():
    print("=== FakeShield v43.0 Scribbr Grade Test ===")
    
    # Test 1: Long Technical Human Text (Research Paper Intro) - ~180 words
    human_text = """
    The rapid proliferation of large language models (LLMs) in academic and professional settings has necessitated the development of robust detection mechanisms. While early detection strategies relied on simple perplexity metrics and N-gram overlap, modern synthetic text has evolved to mimic organic human writing styles with unprecedented fidelity. This research explores the integration of transformer-based classifiers with zero-shot statistical signals to achieve high-precision identification. We analyze the efficacy of the RAID benchmark and examine how stylistic features like part-of-speech entropy and dependency depth can serve as reliable indicators of human authorship. Our experimental results indicate that while neural classifiers provide a strong baseline, they are often susceptible to adversarial humanization techniques. By implementing a multi-layered ensemble approach, we demonstrate a significant improvement in detection accuracy across diverse domains including technical reports and creative writing. This study concludes with a discussion on the ethical implications of automated content moderation and the future of digital provenance in an AI-saturated landscape.
    """ * 2 # Double it to ensure >150 words
    
    # Test 2: Long AI Generated Text (GPT-4o style) - ~200 words
    ai_text = """
    In today's rapidly evolving digital landscape, the rise of artificial intelligence has fundamentally transformed how we interact with technology. From automated customer service bots to advanced data analytics, AI is everywhere. One of the most significant impacts of this technology is seen in the workplace, where automation is streamlining tasks and improving efficiency. However, this shift also raises important questions about the future of human labor and the need for upskilling. In conclusion, while AI offers immense benefits, it is crucial to balance technological progress with ethical considerations to ensure a sustainable future for all. Furthermore, as these systems become more sophisticated, the distinction between human and machine-generated content continues to blur. It is important to note that developers must prioritize transparency and accountability in AI design. Ultimately, the successful integration of artificial intelligence depends on our ability to navigate its complexities with caution and foresight. By fostering a collaborative relationship between humans and machines, we can harness the power of AI to solve some of the world's most pressing challenges.
    """ * 2 # Double it to ensure >150 words

    print("\nWarmup phase (Loading DeBERTa, Binoculars, etc.)...")
    load_models()
    
    print(f"\nAnalyzing Human Text ({len(human_text.split())} words)...")
    res_h = analyze_forensic(human_text)
    print(f"Verdict: {res_h['verdict']} (Score: {res_h['overall_score']})")
    print(f"Details: {res_h['detailed_scores']}")
    print(f"Reasoning: {res_h['reasoning']}")

    print(f"\nAnalyzing AI Text ({len(ai_text.split())} words)...")
    res_a = analyze_forensic(ai_text)
    print(f"Verdict: {res_a['verdict']} (Score: {res_a['overall_score']})")
    print(f"Details: {res_a['detailed_scores']}")
    print(f"Reasoning: {res_a['reasoning']}")

if __name__ == "__main__":
    test_v43()
