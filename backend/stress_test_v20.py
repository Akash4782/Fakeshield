
import requests
import time
import json

API_URL = "http://localhost:8001/api/v1/text/analyze/async"

SAMPLES = [
    {
        "name": "User ML Text (Human)",
        "text": """Machine learning is the subset of artificial intelligence (AI) focused on algorithms that can “learn” the patterns of training data and, subsequently, make accurate inferences about new data. This pattern recognition ability enables machine learning models to make decisions or predictions without explicit, hard-coded instructions. Machine learning has come to dominate the field of AI: it provides the backbone of most modern AI systems, from forecasting models to autonomous vehicles to large language models (LLMs) and other generative AI tools. The central premise of machine learning (ML) is that if you optimize a model’s performance on a dataset of tasks that adequately resemble the real-world problems it will be used for—through a process called model training—the model can make accurate predictions on the new data it sees in its ultimate use case. Training itself is simply a means to an end: generalization, the translation of strong performance on training data to useful results in real-world scenarios, is the fundamental goal of machine learning. In essence, a trained model is applying patterns it learned from training data to infer the correct output for a real-world task: the deployment of an AI model is therefore called AI inference.""",
        "expected": "HUMAN"
    },
    {
        "name": "Research Paper (Human)",
        "text": """This paper presents a novel framework for cross-modal contrastive learning in low-resource environments. We propose an adaptive feature alignment strategy that minimizes the Fréchet Inception Distance (FID) between latent representations of disparate modalities. Our experiments on the benchmark datasets demonstrate a 15% improvement in Top-1 accuracy over state-of-the-art self-supervised methods. Furthermore, we provide a theoretical proof of the convergence properties of our alignment loss under non-convex optimization constraints. The results suggest that temporal consistency plays a crucial role in stabilizing the gradient flow during the early stages of training, particularly when dealing with noisy sparse matrices. We further investigate the impact of weight initialization on the overall stability of the neural network architecture across multiple epochs of stochastic gradient descent. Our findings indicate that properly scaled initialization can prevent the vanishing gradient problem, which is common in deep architectures with multiple non-linear layers. This contribution provides a robust foundation for future research into multi-modal fusion and large-scale generative modeling in diverse and complex environments.""",
        "expected": "HUMAN"
    },
    {
        "name": "Tech Blog (Human)",
        "text": """I've spent the last week diving into the new React 19 features, and honestly, the 'use' hook is a game changer. I remember when we had to wrap everything in useEffect just to fetch a simple JSON, but now the suspense integration feels so much more natural. One thing that tripped me up though was the way it handles promises in the render cycle—you really have to be careful with stable references. If you're building a dashboard with lots of real-time data, I'd definitely recommend checking out how the action transition state works. It's not just about speed; it's about the developer experience being less 'fragile' when managing complex state trees. For instance, I was working on a high-throughput data visualization component and found that the new transition API significantly reduced the number of unnecessary re-renders. It's these subtle performance wins that make the upgrade worth the effort, even if the learning curve feels a bit steep at first. I'm excited to see how the community adopts these patterns in larger production codebases over the coming months as the ecosystem matures.""",
        "expected": "HUMAN"
    },
    {
        "name": "AI Generated (GPT-4)",
        "text": """Machine learning is a subset of artificial intelligence that focuses on the development of algorithms that allow computers to learn from and make decisions based on data. Instead of following static, pre-programmed instructions, these models identify patterns and improve their performance over time. At its core, machine learning involves feeding large amounts of information into a system, which then uses statistical analysis to predict outcomes. This technology is widely used in everything from recommendation engines and self-driving cars to medical diagnosis and financial forecasting. As data becomes more available, machine learning continues to evolve, driving innovation across various industries and transforming how we interact with technology. The primary goal of these systems is to create accurate predictive models that can adapt to new information without human intervention. By leveraging complex mathematical structures such as neural networks and decision trees, machine learning enables computers to solve problems that were previously thought to be impossible for machines. This rapid advancement in computational power and algorithmic efficiency is paving the way for a more automated and data-driven future for all of humanity.""",
        "expected": "AI"
    }
]

def test_engine():
    print("\n" + "="*50)
    print("   FAKESHIELD STRESS TEST (V20.1 - STABLE)")
    print("="*50)

    for s in SAMPLES:
        print(f"\n[TEST] {s['name']}...")
        try:
            # Step 1: Submit job
            resp = requests.post(API_URL, json={"text": s["text"], "mode": "deep"})
            if resp.status_code != 200:
                print(f" ERROR | Status {resp.status_code}: {resp.text}")
                continue
            
            job_data = resp.json()
            job_id = job_data.get("job_id")
            
            # Step 2: Poll for results
            status_url = f"http://localhost:8001/api/v1/text/status/{job_id}"
            max_retries = 30
            result = None
            
            for _ in range(max_retries):
                s_resp = requests.get(status_url)
                s_data = s_resp.json()
                
                if s_data["status"] == "complete":
                    result = s_data["data"]
                    break
                elif s_data["status"] == "error":
                    print(f" ENGINE CRASH: {s_data['data']}")
                    break
                
                time.sleep(2)
            
            if result:
                score = result.get("score", 0)
                verdict = result.get("verdict", "N/A")
                is_ai = score >= 0.65
                
                pass_fail = "PASS" if (is_ai and s["expected"] == "AI") or (not is_ai and s["expected"] == "HUMAN") else "FAIL"
                
                print(f" RESULT | Score: {score:.3f} | Verdict: {verdict} | {pass_fail}")
                print(f" REASON | {result.get('forensic_reasoning', '')[:100]}...")
            else:
                print(" TIMEOUT | Job took too long.")

        except Exception as e:
            print(f" ERROR | Connection failed: {e}")

    print("\n" + "="*50)

if __name__ == "__main__":
    test_engine()
