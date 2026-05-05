from vanguard_diagnostic import ensemble_predict, load_vanguard_v85
import json

load_vanguard_v85()

human_academic = "The intersection of philosophy and technology often reveals deep-seated biases in how we perceive progress. " * 15

print("\n--- HUMAN ACADEMIC DEBUG ---")
res = ensemble_predict(human_academic)
print(json.dumps({
    "overall_score": res["overall_score"],
    "verdict": res["verdict"],
    "signals": res["signals"]
}, indent=2))
