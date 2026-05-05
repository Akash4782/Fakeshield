
import sys
import os
import json

# Add project root to path
sys.path.append(os.getcwd())

from backend.app.models.text_classifier_ensemble import ensemble_predict, load_vanguard_v85

# Sample text from a typical human user (academic style)
human_text = """
The exploration of space has always been a subject of great fascination for humanity. 
From the early days of stargazing to the modern era of planetary rovers and space telescopes, 
our quest to understand the universe has driven technological innovation and expanded our 
philosophical horizons. However, the immense costs associated with space exploration 
often spark debate about its practical benefits compared to pressing issues on Earth. 
Advocates argue that the technologies developed for space—such as satellite communications 
and advanced materials—have revolutionized life on our planet. Furthermore, the 
collaborative nature of international space missions fosters global cooperation 
and scientific advancement that transcends national borders.
""" * 5

print("\n--- TESTING HUMAN TEXT WITH v14.0 ENSEMBLE ---")
res = ensemble_predict(human_text)
print(json.dumps({
    "overall_score": res.get("overall_score"),
    "verdict": res.get("verdict"),
    "signals": res.get("signals"),
    "forensic_reasoning": res.get("forensic_reasoning")
}, indent=2))
