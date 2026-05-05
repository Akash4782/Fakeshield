import torch
from app.models.binoculars import Binoculars

def calibrate_binoculars():
    bino = Binoculars(device="cpu")
    
    human_text = "The rapid development of decentralized finance (DeFi) has created a parallel financial system based on smart contracts and blockchain technology. While it offers transparency and accessibility, it also introduces new risks such as smart contract vulnerabilities and rug pulls. This paper examines the regulatory challenges."
    
    ai_text = "Artificial intelligence has significantly impacted various industries, including healthcare, finance, and education. By automating routine tasks and providing deep insights through data analysis, AI enhances efficiency and productivity. However, ethical concerns regarding privacy and bias remain a major challenge for developers and policymakers."

    print("\n[Human Text] Raw Score:", bino.compute_score(human_text))
    print("[AI Text] Raw Score:", bino.compute_score(ai_text))

if __name__ == "__main__":
    calibrate_binoculars()
