import os
os.environ["HF_HUB_OFFLINE"] = "1"
os.environ["TRANSFORMERS_OFFLINE"] = "1"

print("[Test] Starting offline analysis test...")
from app.models.text_detector import analyze

sample_text = """
Furthermore, machine learning represents a significant paradigm shift in AI.
I went to the market today. The tomatoes looked really fresh and cheap.
In conclusion, it is worth noting that this essay will explore a wide range of rapid advancements.
The history of Rome is filled with glorious conquests and tragic defeats.
"""

if __name__ == "__main__":
    try:
        print("[Test] Calling analyze()...")
        res = analyze(sample_text, include_highlights=True, mode="deep")
        print("\n[Test] SUCCESS!")
        import json
        print(json.dumps({k: v for k, v in res.items() if k != "sentence_highlights"}, indent=2))
        print(f"[Test] Got {len(res['sentence_highlights'])} highlights.")
    except Exception as e:
        import traceback
        print("\n[Test] FAILED:")
        traceback.print_exc()
