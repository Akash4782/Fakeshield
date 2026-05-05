import sys
import os

# Add parent dir to path
sys.path.append(os.getcwd())

from app.models.new_forensic_engine import analyze_forensic, load_models

def run_titan_test():
    print("=== FakeShield Titan Engine v50.0 Integrity Test ===")
    
    # AI Sample (High Quality)
    ai_text = """
    Artificial intelligence has fundamentally transformed how we interact with technology. From automated customer service bots to advanced data analytics, AI is everywhere. One of the most significant impacts of this technology is seen in the workplace, where automation is streamlining tasks and improving efficiency. However, this shift also raises important questions about the future of human labor and the need for upskilling. In conclusion, while AI offers immense benefits, it is crucial to balance technological progress with ethical considerations to ensure a sustainable future for all. Furthermore, developers must prioritize transparency and accountability in AI design to build trust with users. Ultimately, the successful integration of artificial intelligence depends on our ability to navigate its complexities with foresight.
    """ * 2
    
    # Human Sample (Academic/Technical)
    human_text = """
    The integration of distributed ledger technology within supply chain management presents a significant opportunity for enhancing transparency and auditability. By leveraging a decentralized consensus mechanism, stakeholders can verify the provenance of goods without relying on a centralized intermediary. This research explores the scalability constraints of current Ethereum-based solutions when applied to high-throughput logistics environments. We propose a sidechain architecture that offloads transaction volume while maintaining security through periodic state checkpoints on the mainnet. Experimental results indicate a 40% reduction in latency compared to traditional layer-1 implementations. Furthermore, the use of zero-knowledge proofs ensures that sensitive business data remains private while still allowing for verifiable compliance.
    """ * 2

    print("\nWarmup phase...")
    load_models()
    
    print(f"\n[TITAN] Analyzing AI Text ({len(ai_text.split())} words)...")
    res_a = analyze_forensic(ai_text)
    print(f"Verdict: {res_a['verdict']} (Score: {res_a['score']})")
    print(f"Signals: {res_a['detailed_scores']}")
    print(f"Reasoning: {res_a['reasoning']}")
    
    print("\n[SENTENCE HEATMAP - AI]")
    for h in res_a.get('sentence_highlights', [])[:3]:
        print(f"  [{h['label']}] ({h['ai_score']}) {h['sentence'][:60]}...")

    print(f"\n[TITAN] Analyzing Human Text ({len(human_text.split())} words)...")
    res_h = analyze_forensic(human_text)
    print(f"Verdict: {res_h['verdict']} (Score: {res_h['score']})")
    print(f"Signals: {res_h['detailed_scores']}")
    print(f"Reasoning: {res_h['reasoning']}")

    print("\n[SENTENCE HEATMAP - HUMAN]")
    for h in res_h.get('sentence_highlights', [])[:3]:
        print(f"  [{h['label']}] ({h['ai_score']}) {h['sentence'][:60]}...")

if __name__ == "__main__":
    run_titan_test()
