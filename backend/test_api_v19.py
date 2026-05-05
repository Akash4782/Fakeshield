import requests
import json
import time

URL = "http://localhost:8001/api/v1/text/analyze"

SAMPLES = {
    "Wikipedia (Human)": "A large language model (LLM) is a type of artificial intelligence (AI) program that can recognize and generate text, among other tasks. LLMs are trained on immense datasets—hence the 'large' in their name—and are built on neural networks, specifically transformer architectures. These models have revolutionized the field of natural language processing (NLP), enabling applications like chatbots, automated translation, and complex data summarization. By analyzing billions of parameters, LLMs can predict the next word in a sequence with remarkable accuracy, allowing them to produce coherent and contextually relevant prose that often mimics human writing styles. However, the development and deployment of these models come with significant ethical and technical challenges. Concerns about bias in training data, the potential for generating misinformation, and the sheer computational power required for training are central topics in AI research today. As of 2024, the most advanced LLMs, such as GPT-4 and Gemini, are being integrated into professional workflows across diverse industries, from software development to creative writing, fundamentally altering how humans interact with digital information and machine-generated content. Despite their prowess, these models are not truly 'intelligent' in the human sense; they are statistical engines that map linguistic patterns without an internal understanding of the concepts they discuss.",
    "Wikipedia (AI)": "Large language models (LLMs) represent a transformative advancement in the domain of artificial intelligence, particularly within the branch of natural language processing. These sophisticated systems are engineered to understand, interpret, and generate human-like text by processing vast quantities of data. At their core, LLMs utilize deep learning techniques and are predominantly based on the transformer architecture, which facilitates the handling of long-range dependencies in language. This architectural design enables the models to perform a wide array of tasks, including language translation, sentiment analysis, and the creation of highly detailed content. The training process involves exposing the model to massive corpora of text, allowing it to learn the statistical relationships between words and phrases. While the capabilities of modern LLMs are impressive, they are also subject to limitations such as hallucinations, where the model generates factually incorrect information with high confidence. Furthermore, the environmental impact of training these massive models has become a point of significant discussion in the tech community. As the technology continues to evolve, researchers are focusing on making these models more efficient, safer, and better aligned with human values and factual accuracy across all domains."
}

def test_api():
    print("\n" + "="*50)
    print("   FAKESHIELD API VALIDATION (v19.0)")
    print("="*50 + "\n")

    for name, text in SAMPLES.items():
        print(f"[TEST] Sending: {name}...", end="", flush=True)
        try:
            res = requests.post(URL, json={"text": text, "mode": "deep"}, timeout=60)
            data = res.json()
            if data["status"] == "success":
                score = data["data"]["score"]
                verdict = data["data"]["verdict"]
                print(f" DONE | Score: {score} | Verdict: {verdict}")
            else:
                print(f" FAILED | {data}")
        except Exception as e:
            print(f" ERROR | {e}")

if __name__ == "__main__":
    test_api()
