import asyncio
from app.models.text_detector import analyze

sample_text = """
Furthermore, machine learning represents a significant paradigm shift in AI.
I went to the market today. The tomatoes looked really fresh and cheap.
In conclusion, it is worth noting that this essay will explore a wide range of rapid advancements.
The history of Rome is filled with glorious conquests and tragic defeats. The empire stretched across three continents, united by a common language and an unstoppable military machine.
To summarize, it is evident that these models identify patterns that human intelligence alone cannot trace.
"""

if __name__ == "__main__":
    try:
        res = analyze(sample_text, include_highlights=True, mode="deep")
        print("SUCCESS")
        import json
        print(json.dumps(res, indent=2))
    except Exception as e:
        import traceback
        traceback.print_exc()

