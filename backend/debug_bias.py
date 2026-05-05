from vanguard_diagnostic import ensemble_predict, load_vanguard_v85
import json

load_vanguard_v85()

human_research = """
The transformative potential of Large Language Models (LLMs) in clinical settings is contingent upon the alignment of their outputs with medical ontologies. This study investigates the zero-shot performance of GPT-4 and Med-PaLM 2 in identifying rare pathologies from unstructured electronic health records. Our methodology involves a multi-stage prompt engineering approach, utilizing few-shot exemplars to anchor the model's reasoning within specific diagnostic boundaries. Results indicate that while LLMs excel at summarization, their precision in fine-grained entity extraction remains sensitive to noise and formatting inconsistencies. We conclude that a hybrid architecture combining symbolic knowledge graphs with neural transformers is essential for safety-critical medical applications. 
The integration of these systems into existing clinical workflows necessitates a rigorous evaluation of their reliability and interpretability. Previous research has highlighted the risks associated with model hallucinations, particularly in high-stakes environments where diagnostic errors can have severe consequences. By implementing a cross-verification layer, we aim to mitigate these risks and provide clinicians with a more dependable tool for decision support. Furthermore, the ethical considerations surrounding data privacy and model bias must be addressed to ensure equitable access to AI-driven healthcare solutions. Our findings suggest that with proper safeguards, LLMs can significantly enhance the efficiency of medical data processing and improve patient outcomes.
"""

print("\n--- HUMAN RESEARCH RAW SENTENCE DEBUG ---")
res = ensemble_predict(human_research)
print("\nSENTENCE SCORES:")
for s in res["sentence_highlights"]:
    print(f"[{s['label']}] {s['ai_score']}%: {s['sentence']}")

print("\nFINAL SIGNALS:")
print(json.dumps(res["signals"], indent=2))
print(f"OVERALL: {res['overall_score']}")
