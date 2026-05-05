from vanguard_diagnostic import ensemble_predict, load_vanguard_v85
import json

load_vanguard_v85()

# --- DATASET ---
test_suite = [
    {
        "label": "AI",
        "text": "The rapid advancement of artificial intelligence has sparked significant debate regarding its impact on the global workforce. Furthermore, as automation becomes more sophisticated, many traditional roles are being redefined. In conclusion, the need for a comprehensive policy framework is essential to ensure that the transition to an AI-driven economy is equitable. Moreover, we must act now."
    },
    {
        "label": "AI",
        "text": "Climate change represents one of the most pressing challenges of our time. Moreover, the transition to renewable energy sources is a critical step in mitigating its effects. It is important to note that the integration of green technologies into industrial sectors provides a pathway for sustainable growth. Furthermore, international cooperation is essential for achieving climate targets."
    },
    {
        "label": "HUMAN (RESEARCH)",
        "text": "The transformative potential of Large Language Models (LLMs) in clinical settings is contingent upon the alignment of their outputs with medical ontologies. This study investigates the zero-shot performance of GPT-4 and Med-PaLM 2 in identifying rare pathologies from unstructured electronic health records. Our methodology involves a multi-stage prompt engineering approach, utilizing few-shot exemplars to anchor the model's reasoning within specific diagnostic boundaries."
    },
    {
        "label": "HUMAN (BLOG)",
        "text": "I spent the last three weeks traveling through the backroads of the Pacific Northwest, and honestly, it changed my perspective on solo hiking. The air was crisp, the trails were empty, and the silence was almost deafening. It wasn't about the destination or the summit photos; it was about the small moments—the smell of cedar after rain, the sound of a distant creek, and the feeling of complete independence."
    },
    {
        "label": "HUMAN (TECHNICAL)",
        "text": "To configure the Nginx load balancer, we first need to define the upstream server block within the global configuration file. This ensures that incoming traffic is distributed across the three backend nodes using a round-robin algorithm. We then set the proxy_pass directive to point to this upstream group, while also enabling keep-alive connections to minimize latency during peak traffic periods."
    }
]

print("\n--- VANGUARD FORENSIC BENCHMARK (Titan-v85.15) ---")
results = []
correct = 0

for item in test_suite:
    res = ensemble_predict(item["text"])
    pred = "AI" if res["verdict"] == "AI GENERATED" else "HUMAN"
    expected = "AI" if item["label"].startswith("AI") else "HUMAN"
    
    is_correct = pred == expected
    if is_correct: correct += 1
    
    results.append({
        "type": item["label"],
        "score": res["overall_score"],
        "verdict": res["verdict"],
        "result": "PASSED" if is_correct else "FAILED"
    })

accuracy = (correct / len(test_suite)) * 100
print(json.dumps(results, indent=2))
print(f"\nFINAL ACCURACY: {accuracy:.2f}%")
