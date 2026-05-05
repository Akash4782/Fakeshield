from vanguard_diagnostic import ensemble_predict, load_vanguard_v85
import json

load_vanguard_v85()

ai_text = """
The intersection of economic policy and sustainable development is a critical area of study for modern governments. Furthermore, the implementation of carbon tax initiatives underscores the importance of fiscal responsibility in environmental management. Moreover, the integration of green technologies into industrial sectors provides a pathway for long-term growth. In conclusion, a coordinated approach between public and private sectors is essential for achieving climate targets. Furthermore, the emergence of smart grids and decentralized energy systems has revolutionized the way we consume and distribute power. These advancements not only enhance efficiency but also empower local communities to take control of their energy needs.
Organizations must establish robust frameworks to ensure that the transition to a low-carbon economy is both inclusive and equitable. As we move forward, the synergy between technological innovation and policy reform will likely define the next era of environmental stewardship. This collaborative approach can lead to innovative solutions for complex global challenges, ranging from climate mitigation to sustainable urban planning. Ultimately, the successful deployment of green technologies depends on our ability to balance economic growth with environmental preservation. Furthermore, the global community must unite to address the transboundary nature of climate change, fostering international cooperation and knowledge sharing.
"""

human_text = """
The transformative potential of Large Language Models (LLMs) in clinical settings is contingent upon the alignment of their outputs with medical ontologies. This study investigates the zero-shot performance of GPT-4 and Med-PaLM 2 in identifying rare pathologies from unstructured electronic health records. Our methodology involves a multi-stage prompt engineering approach, utilizing few-shot exemplars to anchor the model's reasoning within specific diagnostic boundaries. Results indicate that while LLMs excel at summarization, their precision in fine-grained entity extraction remains sensitive to noise and formatting inconsistencies. We conclude that a hybrid architecture combining symbolic knowledge graphs with neural transformers is essential for safety-critical medical applications. Previous research has highlighted the risks associated with model hallucinations, particularly in high-stakes environments where diagnostic errors can have severe consequences.
By implementing a cross-verification layer, we aim to mitigate these risks and provide clinicians with a more dependable tool for decision support. Furthermore, the ethical considerations surrounding data privacy and model bias must be addressed to ensure equitable access to AI-driven healthcare solutions. Our findings suggest that with proper safeguards, LLMs can significantly enhance the efficiency of medical data processing and improve patient outcomes. However, the integration of such models requires a cautious approach, balancing innovation with rigorous clinical validation and transparency. Future work will explore the scalability of this hybrid framework across larger datasets and its impact on clinical decision-making in diverse healthcare environments.
"""

print("\n--- TEST 1: AI DETECTION (TITAN-v85.10) ---")
res1 = ensemble_predict(ai_text)
print(json.dumps(res1, indent=2))

print("\n--- TEST 2: HUMAN PROTECTION (TITAN-v85.10) ---")
res2 = ensemble_predict(human_text)
print(json.dumps(res2, indent=2))
