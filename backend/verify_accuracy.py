import sys
import os

# Add the current directory to sys.path to import app
sys.path.append(os.getcwd())

from app.models.text_classifier_ensemble import ensemble_predict

# 1. AI GENERATED TEXT (Classic GPT-3.5 repetitive style)
ai_text = """
The use of technology in education has many benefits for students. Firstly, it allows students to access a vast amount of information from the internet. Secondly, it encourages students to develop their digital skills, which are important for their future careers. In addition, technology can make learning more engaging and interactive. Therefore, it is clear that technology plays a crucial role in modern education.
"""

# 2. HUMAN WRITTEN TEXT (Informal, slangy)
human_text = """
dude you wont believe what happened at the park today. so there was this guy juggling chainsaws but like he was actually good at it until a squirrel ran across his feet. he didnt get hurt but he dropped everything and it was just super chaotic and funny to watch lol. i wish i recorded it on my phone but it died like ten minutes before.
"""

def test_text(label, text):
    print(f"\n--- Testing {label} ---")
    result = ensemble_predict(text, mode="deep")
    print(f"Verdict: {result['verdict']}")
    print(f"Score: {result['score'] * 100}%")
    print(f"Confidence: {result['confidence']}")
    print(f"Signals: {result['signals']}")
    if 'binoculars_details' in result:
        print(f"Bino Raw Score: {result['binoculars_details'].get('score')}")

if __name__ == "__main__":
    print("FAKESHIELD ACCURACY VERIFICATION (v15.0)")
    test_text("AI TEXT", ai_text)
    test_text("HUMAN TEXT", human_text)
