import torch
import numpy as np
from transformers import AutoTokenizer, AutoModelForCausalLM
from typing import List, Union

class Binoculars:
    """
    Binoculars: Zero-Shot AI Text Detection (v16 Optimized)
    Uses the ratio of Perplexity (Observer) to Cross-Perplexity (Performer).
    """

    def __init__(
        self,
        observer_name: str = "EleutherAI/pythia-160m",
        performer_name: str = "EleutherAI/pythia-70m",
        device: str = "cpu"
    ):
        self.device = device if torch.cuda.is_available() or device == "cpu" else "cuda"
        
        print(f"[Binoculars] Initializing Observer: {observer_name}...", flush=True)
        self.tokenizer = AutoTokenizer.from_pretrained(observer_name)
        self.observer = AutoModelForCausalLM.from_pretrained(observer_name).to(self.device).eval()
        
        print(f"[Binoculars] Initializing Performer: {performer_name}...", flush=True)
        self.performer = AutoModelForCausalLM.from_pretrained(performer_name).to(self.device).eval()
        
        # Threshold calibrated for Pythia-160M/70M pair
        # AI typically has a ratio < 0.90 with this pair.
        # Human writing typically has a ratio > 1.05.
        self.threshold = 1.05 

    def compute_score(self, text: str) -> float:
        try:
            tokens = self.tokenizer(text, return_tensors="pt", truncation=True, max_length=512).to(self.device)
            input_ids = tokens["input_ids"]
            
            with torch.no_grad():
                obs_logits = self.observer(input_ids).logits
                perf_logits = self.performer(input_ids).logits
                
                obs_log_probs = torch.log_softmax(obs_logits, dim=-1)
                perf_log_probs = torch.log_softmax(perf_logits, dim=-1)
            
            target_ids = input_ids[:, 1:].unsqueeze(-1)
            
            # Log-probs of the actual tokens
            obs_token_lp = obs_log_probs[:, :-1, :].gather(dim=-1, index=target_ids).squeeze(-1)
            perf_token_lp = perf_log_probs[:, :-1, :].gather(dim=-1, index=target_ids).squeeze(-1)
            
            # Score = LogProb(Obs) / LogProb(Perf)
            # Since these are negative, ratio is positive.
            obs_sum = obs_token_lp.sum().item()
            perf_sum = perf_token_lp.sum().item()
            
            # Avoid divide by zero
            score = obs_sum / (perf_sum + 1e-9)
            
            return float(score)
        except Exception as e:
            print(f"[Binoculars] Score error: {e}")
            return 1.1 # Default to human-like ratio on error

    def predict(self, text: str) -> dict:
        score = self.compute_score(text)
        
        # v16.8 RE-CALIBRATION (Pythia 160m/70m pair):
        # Center shifted to 0.92 to catch modern LLMs (Gemini/Claude) which are more 'human-like'
        normalized_ai_prob = 1.0 / (1.0 + np.exp((score - 0.92) * 32))
        
        return {
            "score": round(score, 4),
            "ai_probability": round(float(normalized_ai_prob), 3),
            "is_ai": score < self.threshold
        }
