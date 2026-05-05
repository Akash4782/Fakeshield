import sys
import os

# Add parent dir to path
sys.path.append(os.getcwd())

from app.models.new_forensic_engine import analyze_forensic, load_models

def verify_fix():
    print("=== Titan Engine v51.0 Sensitivity Verification ===")
    load_models()

    # Highly structured AI sample (GPT-4o style)
    # This is the kind of text that Scribbr catches at 97%
    ai_text = """
    The integration of sustainable energy practices within urban infrastructure is a critical component of modern environmental strategy. As global temperatures continue to rise, cities must pivot away from fossil fuel dependence and toward renewable sources such as solar, wind, and geothermal energy. This transition is not merely a matter of technological implementation but also involves comprehensive policy reform and public engagement. Furthermore, the decentralization of energy grids allows for greater resilience in the face of natural disasters, which are becoming increasingly frequent due to climate change. One of the most effective ways to achieve this is through the implementation of smart grids that optimize energy distribution based on real-time demand. In conclusion, the successful adoption of green technology requires a multi-faceted approach that balances economic growth with ecological preservation. By prioritizing sustainability, urban centers can serve as models for global progress in the fight against environmental degradation.
    """ * 2 # To pass 150 word gate

    print("\n[TEST] Analyzing High-Sensitivity AI Sample...")
    res = analyze_forensic(ai_text)
    
    print(f"Verdict: {res['verdict']}")
    print(f"Overall Score: {res['score']}")
    print(f"Neural (DeBERTa): {res['detailed_scores']['deberta']}")
    print(f"Math (Binoculars): {res['detailed_scores']['binoculars']}")
    print(f"Logic used: {res['fingerprint']}")
    
    if res['detailed_scores']['deberta'] > 0.8:
        print("\n✅ SUCCESS: DeBERTa signal is now high-sensitivity.")
    else:
        print("\n❌ FAILURE: Sensitivity still too low.")

if __name__ == "__main__":
    verify_fix()
