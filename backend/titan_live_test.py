import sys
import os

# Add parent dir to path
sys.path.append(os.getcwd())

from app.models.new_forensic_engine import analyze_forensic, load_models

def run_live_test():
    print("=== FakeShield Titan Engine v50.0 — Live Authorship Test ===")
    load_models()

    # 1. Fresh Human Sample (Anecdotal/Philosophical)
    human_text = """
    I was walking through the park the other day, thinking about how we define 'intelligence' in this age of silicon. It's funny, really. We spend so much time trying to make machines act like us, but we rarely stop to ask if we’re starting to act like them. My grandfather used to say that a true conversation isn't just about exchanging information; it's about the silence between the words—the pauses where we actually listen. You can't program a pause. You can program a delay, sure, but a pause is an act of will, a choice to wait. It’s that choice, that inherent unpredictability of the human spirit, that seems to be the one thing our code can’t quite capture. When I look at the way my daughter plays with her blocks, there’s no optimization. There’s no objective function. It’s just pure, unadulterated exploration for the sake of it. Maybe that's the secret. Intelligence isn't about solving the problem the fastest; it's about being curious enough to create the problem in the first place, just to see what happens next.
    """ * 2

    # 2. Fresh AI Sample (Academic Summary)
    ai_text = """
    The Industrial Revolution was a period of significant economic and social transformation that began in Great Britain during the late 18th century. It marked a shift from an agrarian and handicraft-based economy to one dominated by machine manufacturing and the factory system. Several key factors contributed to this transition, including the development of new technologies, the availability of natural resources like coal and iron, and a growing population that provided both labor and a market for manufactured goods. One of the most important inventions of this era was the steam engine, which provided a reliable and versatile source of power for factories and transportation. Furthermore, the expansion of the British Empire facilitated access to raw materials and international markets. In conclusion, the Industrial Revolution fundamentally altered the structure of society, leading to urbanization and the rise of the middle class, while also presenting new challenges regarding labor conditions and environmental impact.
    """ * 2

    print("\n[ANALYZING HUMAN SAMPLE]...")
    res_h = analyze_forensic(human_text)
    print(f"Verdict: {res_h['verdict']}")
    print(f"Score:   {res_h['score']}")
    print(f"Reasoning: {res_h['reasoning']}")

    print("\n[ANALYZING AI SAMPLE]...")
    res_a = analyze_forensic(ai_text)
    print(f"Verdict: {res_a['verdict']}")
    print(f"Score:   {res_a['score']}")
    print(f"Reasoning: {res_a['reasoning']}")

if __name__ == "__main__":
    run_live_test()
