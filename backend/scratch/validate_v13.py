"""
Live validation of Ensemble Engine v13.0 using the async endpoint.
"""
import requests, time, json

BASE_URL = "http://localhost:8001"
TIMEOUT  = 300  # 5 minutes for CPU

AI_TEXT = (
    "Machine learning is a subset of artificial intelligence that enables systems to learn and improve "
    "from experience without being explicitly programmed. It focuses on developing computer programs that "
    "can access data and use it to learn for themselves. The process begins with observations or data, such "
    "as examples, direct experience, or instruction, so that computers can learn to make better decisions "
    "based on the patterns they find in the data. The primary aim is to allow computers to learn automatically "
    "without human intervention or assistance and adjust actions accordingly. There are three main types of "
    "machine learning: supervised learning, unsupervised learning, and reinforcement learning. Supervised "
    "learning involves training a model on labeled data, where the correct answers are provided. Unsupervised "
    "learning deals with unlabeled data, and the model tries to find hidden patterns or intrinsic structures "
    "in the input. Reinforcement learning is based on rewarding desired behaviors and punishing undesired ones. "
    "Recommendation systems on platforms like Netflix or Spotify suggest content based on your behavior. "
    "Fraud detection systems in banks identify suspicious transactions."
)

HUMAN_TEXT = (
    "I honestly couldn't sleep last night — kept tossing around this problem. Tried three different approaches "
    "and none of them really felt right. The third one was almost there, but then the edge cases just wrecked "
    "everything. My friend suggested ignoring those cases entirely but that feels deeply wrong. Anyway, "
    "I'm going back to basics tomorrow. Need coffee first though, it's been a rough week. The whole thing "
    "started when my manager asked me to just 'quickly' fix the pipeline — yeah, right. Two days later "
    "and I'm still here staring at logs that make no sense whatsoever."
)

def submit_async(text, name):
    r = requests.post(
        f"{BASE_URL}/api/v1/text/analyze/async",
        json={"text": text, "mode": "deep"},
        timeout=30
    )
    job_id = r.json().get("job_id")
    print(f"[{name}] Submitted → job_id={job_id}")
    return job_id

def poll(job_id, name, max_wait=300):
    deadline = time.time() + max_wait
    while time.time() < deadline:
        r = requests.get(f"{BASE_URL}/api/v1/text/status/{job_id}", timeout=15)
        data = r.json()
        if data.get("status") == "complete":
            d = data.get("data", {})
            print(f"\n{'='*55}")
            print(f"  [{name}]")
            print(f"  Verdict:    {d.get('verdict')}")
            print(f"  AI Score:   {round(d.get('score', 0)*100, 1)}%")
            print(f"  Threat:     {d.get('threat_level')}")
            print(f"  Confidence: {d.get('confidence')}")
            layers = d.get('layer_breakdown', {})
            print(f"  HC3:        {round(layers.get('hc3_chatgpt_detector', 0)*100, 1)}%")
            print(f"  PPL:        {round(layers.get('gpt2_perplexity', 0)*100, 1)}%")
            print(f"  Burstiness: {round(layers.get('gpt2_burstiness', 0)*100, 1)}%")
            print(f"  Binoculars: {round(layers.get('binoculars', 0)*100, 1)}%")
            raw = d.get('raw_metrics', {})
            print(f"  Perplexity: {raw.get('perplexity', '?')}")
            print(f"  Burstiness: {raw.get('burstiness', '?')}")
            print(f"  Reason:     {d.get('reasons', [''])[0][:120]}")
            return
        elif data.get("status") == "error":
            print(f"[{name}] ERROR: {data.get('data')}")
            return
        time.sleep(3)
    print(f"[{name}] TIMEOUT after {max_wait}s")

job1 = submit_async(AI_TEXT, "AI-GENERATED ML text")
job2 = submit_async(HUMAN_TEXT, "HUMAN personal text")

print("\nPolling results...")
poll(job1, "AI-GENERATED ML text")
poll(job2, "HUMAN personal text")
