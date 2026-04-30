from app.models.forensic_judge import ForensicJudge
from dotenv import load_dotenv
import os

load_dotenv()

print("Testing updated ForensicJudge...")
judge = ForensicJudge()

if judge.enabled:
    print(f"Judge initialized with {judge.active_model}")
    res = judge.evaluate("This is a test of the forensic reasoning system.", {"neural": 85, "perplexity": 12})
    print(f"Result: {res}")
else:
    print("Judge is still disabled.")
