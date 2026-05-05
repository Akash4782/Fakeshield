import sys
import os

# Add parent dir to path
sys.path.append(os.getcwd())

from app.models.new_forensic_engine import analyze_forensic, load_models

def test_engine():
    print("=== FakeShield v42.0 Research Absolute Test ===")
    
    # Test 1: Technical Human Text (Research-like)
    human_text = """
    The integration of distributed ledger technology within supply chain management presents a significant opportunity for enhancing transparency and auditability. By leveraging a decentralized consensus mechanism, stakeholders can verify the provenance of goods without relying on a centralized intermediary. This research explores the scalability constraints of current Ethereum-based solutions when applied to high-throughput logistics environments. We propose a sidechain architecture that offloads transaction volume while maintaining security through periodic state checkpoints on the mainnet. Experimental results indicate a 40% reduction in latency compared to traditional layer-1 implementations.
    """
    
    # Test 2: AI Generated Text (GPT-4o style)
    ai_text = """
    In today's rapidly evolving digital landscape, the rise of artificial intelligence has fundamentally transformed how we interact with technology. From automated customer service bots to advanced data analytics, AI is everywhere. One of the most significant impacts of this technology is seen in the workplace, where automation is streamlining tasks and improving efficiency. However, this shift also raises important questions about the future of human labor and the need for upskilling. In conclusion, while AI offers immense benefits, it is crucial to balance technological progress with ethical considerations to ensure a sustainable future for all.
    """

    print("\nWarmup phase...")
    load_models()
    
    print("\nAnalyzing Human Text...")
    res_h = analyze_forensic(human_text)
    print(f"Verdict: {res_h['verdict']} (Score: {res_h['overall_score']})")
    print(f"Details: {res_h['detailed_scores']}")
    print(f"Reasoning: {res_h['reasoning']}")

    print("\nAnalyzing AI Text...")
    res_a = analyze_forensic(ai_text)
    print(f"Verdict: {res_a['verdict']} (Score: {res_a['overall_score']})")
    print(f"Details: {res_a['detailed_scores']}")
    print(f"Reasoning: {res_a['reasoning']}")

if __name__ == "__main__":
    test_engine()
