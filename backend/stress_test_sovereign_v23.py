
import requests
import time
import json

API_URL = "http://localhost:8001/api/v1/text/analyze/async"

SAMPLES = [
    {
        "name": "Technical Definition (Human)",
        "text": """Machine learning is the subset of artificial intelligence (AI) focused on algorithms that can “learn” the patterns of training data and, subsequently, make accurate inferences about new data. This pattern recognition ability enables machine learning models to make decisions or predictions without explicit, hard-coded instructions. Machine learning has come to dominate the field of AI: it provides the backbone of most modern AI systems, from forecasting models to autonomous vehicles to large language models (LLMs) and other generative AI tools. The central premise of machine learning (ML) is that if you optimize a model’s performance on a dataset of tasks that adequately resemble the real-world problems it will be used for—through a process called model training—the model can make accurate predictions on the new data it sees in its ultimate use case. Training itself is simply a means to an end: generalization, the translation of strong performance on training data to useful results in real-world scenarios, is the fundamental goal of machine learning. In essence, a trained model is applying patterns it learned from training data to infer the correct output for a real-world task: the deployment of an AI model is therefore called AI inference.""",
        "expected": "HUMAN"
    },
    {
        "name": "Research Abstract (Human)",
        "text": """This study explores the synergistic relationship between reinforcement learning from human feedback (RLHF) and direct preference optimization (DPO) in the context of large-scale language model alignment. We demonstrate that while RLHF provides a broad foundational alignment, DPO is significantly more efficient at fine-tuning specific stylistic nuances. Our methodology involves a bifurcated training pipeline where the model is first exposed to a massive corpus of diverse human preferences before being distilled using a specialized DPO loss function. The empirical results show a 12% reduction in hallucinatory outputs compared to standard proximal policy optimization methods. Furthermore, we provide a qualitative analysis of the reward hacking behaviors observed during the early stages of the RLHF phase, suggesting that careful reward shaping is essential for maintaining semantic integrity across high-entropy generation tasks.""",
        "expected": "HUMAN"
    },
    {
        "name": "AI Generated (GPT-4o)",
        "text": """Machine learning is a transformative subset of artificial intelligence that empowers computers to learn from data without being explicitly programmed. By utilizing various statistical techniques and neural networks, these systems can identify complex patterns and make highly accurate predictions about future outcomes. The process typically begins with data collection and preprocessing, followed by the selection of a suitable algorithm—such as a random forest or a deep transformer—that can best capture the underlying relationships within the dataset. As more information is processed, the model iteratively refines its internal parameters, leading to improved performance and higher reliability. This technology is now at the heart of many modern innovations, including personalized recommendations, medical image analysis, and the development of autonomous systems that can safely navigate complex urban environments without human oversight. Its ability to scale across diverse industries makes it one of the most critical drivers of the current digital revolution.""",
        "expected": "AI"
    },
    {
        "name": "Paraphrased AI (Human-Modified)",
        "text": """Look, machine learning is basically just teaching computers how to spot patterns in data without writing a million lines of 'if-else' statements. It's the engine behind things like ChatGPT or those self-driving cars you see on the news. The whole idea is to take a giant pile of data, throw it at a model during 'training', and hope it learns enough to guess the right answer when it sees something new. It's not magic, it's just math and a lot of trial and error. If you get the training data right, the model gets really good at generalizing to real-world stuff. If you mess up the data, you get bad results. It's as simple as that. We're seeing this tech pop up everywhere lately, and it's definitely changing how we think about automation in our daily lives.""",
        "expected": "HUMAN" # (Heavily paraphrased/casual should be safe)
    }
]

def run_test():
    print("\n" + "="*60)
    print("   FAKESHIELD V23 'SOVEREIGN' SOVEREIGN TEST")
    print("="*60)

    for s in SAMPLES:
        print(f"\n[TEST] {s['name']}...")
        try:
            resp = requests.post(API_URL, json={"text": s["text"], "mode": "deep"})
            job_id = resp.json().get("job_id")
            
            status_url = f"http://localhost:8001/api/v1/text/status/{job_id}"
            result = None
            for _ in range(30):
                s_resp = requests.get(status_url)
                s_data = s_resp.json()
                if s_data["status"] == "complete":
                    result = s_data["data"]
                    break
                elif s_data["status"] == "error":
                    print(f" ERROR: {s_data['data']}")
                    break
                time.sleep(2)
            
            if result:
                score = result.get("score", 0)
                verdict = result.get("verdict", "N/A")
                is_ai = score >= 0.70
                is_human = score < 0.25
                
                status = "FAIL"
                if s["expected"] == "AI" and is_ai: status = "PASS"
                if s["expected"] == "HUMAN" and is_human: status = "PASS"
                if s["expected"] == "HUMAN" and not is_ai and score < 0.65: status = "PASS (SAFE)"

                print(f" RESULT | Score: {score:.3f} | Verdict: {verdict} | {status}")
                print(f" SIGNALS| {result.get('signals', {})}")
            else:
                print(" TIMEOUT")
        except Exception as e:
            print(f" CRASH: {e}")

    print("\n" + "="*60)

if __name__ == "__main__":
    run_test()
