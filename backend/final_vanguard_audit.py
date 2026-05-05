import sys
import os

# Add parent dir to path
sys.path.append(os.getcwd())

from app.models.new_forensic_engine import analyze_forensic, load_models

def run_final_audit():
    print("=== FakeShield Vanguard v60.0 — Sovereign Final Audit ===")
    load_models()

    samples = [
        {
            "name": "Standard AI (GPT-4o)",
            "text": "Artificial intelligence has rapidly evolved over the last decade, transitioning from simple rule-based systems to complex neural networks. One of the most significant breakthroughs has been the development of large language models, which are capable of generating human-like text by predicting the next token in a sequence. These models are trained on massive datasets and can perform a wide variety of tasks, including translation, summarization, and coding. However, as AI becomes more prevalent, concerns regarding bias, misinformation, and job displacement have intensified. It is crucial for developers and policymakers to collaborate on ethical frameworks that ensure the responsible deployment of these powerful technologies. In conclusion, while AI offers immense potential for innovation, it also requires careful oversight to mitigate potential risks and maximize its benefits for society at large." * 2
        },
        {
            "name": "Academic Human",
            "text": "The efficacy of decentralized consensus mechanisms in permissionless blockchain systems is often constrained by the trilemma of security, scalability, and decentralization. While Proof of Work (PoW) provides robust security through computational difficulty, it suffers from excessive energy consumption and low transaction throughput. Conversely, Proof of Stake (PoS) offers a more sustainable alternative but introduces challenges related to initial stake distribution and 'nothing at stake' problems. This paper examines the role of Sharding and Layer-2 protocols in mitigating these bottlenecks. By partitioning the state and parallelizing transaction processing, these techniques aim to achieve horizontal scalability without compromising the underlying security properties of the network. Our findings suggest that a hybrid approach, combining zero-knowledge proofs with optimistic rollups, provides the most viable path toward a global-scale financial infrastructure." * 2
        },
        {
            "name": "Humanized AI (Stealth Mode)",
            "text": "I really think we need to talk about how AI is changing everything. It's not just about the gadgets anymore; it's about how we interact with the world around us. Urban environments are in a unique position to lead the way in sustainable energy. Imagine solar panels on every single rooftop and wind turbines catching every breeze. It sounds like science fiction, but it's becoming our reality. We need policies that actually work for people and a collective will to see them through. If we decentralize the energy grid, we'll be much safer when those big storms hit, and they're hitting more often than ever. Smart grids are the future because they can manage power in real-time. Basically, it's a huge puzzle where we have to balance making a living with keeping our planet healthy. Cities can show everyone else how it's done." * 2
        },
        {
            "name": "Short Human (Under Gate)",
            "text": "This is a short sentence written by a human. It's not long enough to be forensic."
        }
    ]

    for s in samples:
        print(f"\n[AUDIT: {s['name']}]")
        res = analyze_forensic(s['text'])
        print(f"Verdict: {res['verdict']}")
        print(f"Score:   {res['score']}")
        if "detailed_scores" in res:
            print(f"Signals: {res['detailed_scores']}")
        print(f"Time:    {res['processing_time']}")

if __name__ == "__main__":
    run_final_audit()
