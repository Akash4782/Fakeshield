import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from app.models.new_forensic_engine import analyze_forensic as analyze

text = """Joanna Paresi was the last one left – the last living person in a family who had been market traders for hundreds of years. She was born at the foot of the mountains that stood over her home like giants, and she had lived there all her life. On the highest of those mountains, the stone fruit grew. Late in the year, the fruit fell. Most of it rolled and fell down the mountains and was never seen again. But some rolled down into a small valley, hidden deep in the mountains. Joanna's family were the only people who knew about the valley.

When the stone fruit dropped from the trees, they were black and hard. Over four long months, they slowly turned from black to grey and, at last, to silver. Then their skin would break open easily to show the sweet, sun-coloured fruit inside.

When they were ripe, the stone fruit were the most popular food in the whole region. On market day, people got up really early and queued for hours to buy them. Joanna's family always had more to sell than anyone else. The fruit had made her family plenty of money over the years, but they were not as wealthy as the farmers."""

print("Testing text:")
print(text[:100] + "...\n")
result = analyze(text, mode="deep")

print("\n" + "="*50)
print(f"Verdict: {result['verdict']} ({result['confidence']}%)")
print("Signals:")
for k, v in result['signals'].items():
    print(f"  {k}: {v}%")
    
print(f"\nForensic Reasoning:\n{result.get('forensic_reasoning', 'N/A')}")
    
if result.get('sentence_highlights'):
    print("\nHighlights:")
    for h in result['sentence_highlights']:
        if h.get('label') != 'HUMAN' and h.get('label') != 'too_short':
            print(f"  [{h['label']}] ({h['ai_score']}%) {h['sentence']}")
print("="*50 + "\n")
