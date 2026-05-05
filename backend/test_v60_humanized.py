import sys
import os

# Add parent dir to path
sys.path.append(os.getcwd())

from app.models.new_forensic_engine import analyze_forensic, load_models

def test_v60_vanguard():
    print("=== FakeShield Vanguard v60.0 — The 2026 Stress Test ===")
    
    # 1. 'Humanized' AI Text (Rewritten by a human-style prompt)
    # This text is grammatically perfect but has 'Robotic Rhythm' and 'Semantic Compression'
    humanized_ai = """
    Listen, the way the climate is shifting these days isn't just some small thing we can ignore anymore. Urban centers across the globe are starting to realize that if they don't change how they handle energy, they're going to be in deep trouble. We're talking about moving away from coal and oil entirely, and instead, looking at things like solar panels on every roof and wind turbines wherever the breeze hits right. It's not just about the tech, though. You need policies that actually make sense and people who are willing to get on board with the plan. Plus, if we make the grid decentralized, it won't just fail all at once when a big storm hits—which is happening way too often lately. Smart grids are basically the only way forward because they can figure out where the power needs to go in real-time. To wrap it up, going green is a massive puzzle that needs to balance making money with keeping the planet alive. Urban areas have a real chance to lead the way here.
    """ * 2

    print("\n[VANGUARD] Analyzing Humanized AI Text...")
    res = analyze_forensic(humanized_ai)
    
    print(f"Verdict: {res['verdict']}")
    print(f"Overall Score: {res['score']}")
    print(f"Signals: {res['detailed_scores']}")
    print(f"Reasoning: {res['reasoning']}")
    print(f"Logic: {res['fingerprint']}")
    
    if "AI" in res['verdict'].upper():
        print("\n✅ VANGUARD SUCCESS: Caught the humanized AI text.")
    else:
        print("\n❌ VANGUARD FAILURE: Still being tricked by humanization.")

if __name__ == "__main__":
    test_v60_vanguard()
