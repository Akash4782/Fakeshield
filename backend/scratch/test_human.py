import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.models.new_forensic_engine import analyze_forensic as analyze

human_text = """I remember when I first started learning about computer science. It wasn't about the flashy apps or the high-paying jobs back then. It was the simple curiosity of how a machine could understand logic. I spent hours in my room, typing away on an old keyboard, trying to make sense of C++ syntax. It was frustrating, sure, but the moment my first program actually ran—a simple calculator that added two numbers—I felt like I had discovered a superpower. That raw excitement is something that AI just can't replicate. It's the human struggle, the late nights of trial and error, and the personal satisfaction of overcoming a hurdle that defines our relationship with technology. Even today, when everything is automated and AI can generate code in seconds, I still find myself going back to the basics, just to feel that connection to the craft. There's a soul in hand-written code and hand-written stories that no algorithm can ever truly mimic."""

result = analyze(human_text, mode="deep")
print(f"SCORE: {result['score']}")
print(f"VERDICT: {result['verdict']}")
print(f"HUMAN SHIELD: {result['signals'].get('human_shield', 'N/A')}")
for k, v in result['signals'].items():
    print(f"  {k}: {v}")
