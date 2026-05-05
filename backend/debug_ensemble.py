import json
from vanguard_diagnostic import ensemble_predict, load_vanguard_v85

load_vanguard_v85()

ai_text = """
Furthermore, it is important to note that artificial intelligence underscores the importance of data ethics.
In conclusion, the optimization of neural networks requires a multi-faceted approach to convergence.
The implementation of blockchain technology in supply chain management offers unprecedented transparency.
Moreover, the integration of renewable energy sources into the grid poses significant logistical challenges.
Artificial intelligence has fundamentally transformed how we interact with information and technology.
""" * 10 

res = ensemble_predict(ai_text)
print(json.dumps({
    "overall_score": res["overall_score"],
    "verdict": res["verdict"],
    "signals": res["signals"],
    "confidence": res["confidence"]
}, indent=2))
