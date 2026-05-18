import torch
import numpy as np
from transformers import AutoTokenizer, AutoModelForCausalLM, AutoConfig
from typing import List, Union

class Binoculars:
    """
    Binoculars: Zero-Shot AI Text Detection (v16 Optimized)
    Uses the ratio of Perplexity (Observer) to Cross-Perplexity (Performer).
    """

    def __init__(self, observer_name="EleutherAI/pythia-70m", performer_name="EleutherAI/pythia-160m", device="cpu"):
        self.device = device
        self.tokenizer = None
        self.observer = None
        self.performer = None
        self.enabled = False
        self.threshold = 0.97
        
        try:
            print(f"[Binoculars] Eager-Loading Observer: {observer_name}...", flush=True)
            self.tokenizer = AutoTokenizer.from_pretrained(observer_name)
            
            # CRITICAL FIX: Use explicit device_map to prevent meta-tensor errors
            self.observer = AutoModelForCausalLM.from_pretrained(
                observer_name,
                low_cpu_mem_usage=True,
                device_map={"": self.device},
                torch_dtype=torch.float32,
            ).eval()
            
            print(f"[Binoculars] Eager-Loading Performer: {performer_name}...", flush=True)
            self.performer = AutoModelForCausalLM.from_pretrained(
                performer_name,
                low_cpu_mem_usage=True,
                device_map={"": self.device},
                torch_dtype=torch.float32,
            ).eval()
            
            self.threshold = 0.97 
            self.enabled = True
            print("[Binoculars] Sovereign Engine ONLINE.", flush=True)
        except Exception as e:
            print(f"[Binoculars] FAILED to initialize: {e}. Falling back to 4-signal ensemble.", flush=True)
            self.enabled = False

    def compute_score(self, text: str) -> float:
        if not self.enabled:
            return 0.5
        try:
            tokens = self.tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
            if self.device != "cpu":
                tokens = tokens.to(self.device)
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
            
            # Binoculars Score = log_prob(performer) / log_prob(observer)
            # For AI text, performer predicts better (log_prob closer to 0), 
            # so the ratio is smaller than for human text.
            obs_sum = obs_token_lp.sum().item()
            perf_sum = perf_token_lp.sum().item()
            
            # Use the correct Binoculars ratio: Performer / Observer
            score = perf_sum / (obs_sum + 1e-9)
            
            return float(score)
        except Exception as e:
            print(f"[Binoculars] Score error: {e}")
            return 1.0 # Default to human-like ratio on error

    def predict(self, text: str) -> dict:
        score = self.compute_score(text)
        
        # Observed score ranges (pythia-70m observer / pythia-160m performer):
        #   AI text  : score ~ 0.87 - 0.93  (performer NOT better than observer)
        #   Human text: score ~ 0.97 - 1.05  (performer better = higher ratio)
        # Rule: LOWER score = MORE AI-like.
        # Threshold calibrated at 0.95 (midpoint between AI and human ranges).
        threshold = 0.95
        
        # Inverted sigmoid: low score → high ai_probability
        # Multiply by -30 so values tightly cluster around threshold
        normalized_ai_prob = 1.0 / (1.0 + np.exp((score - threshold) * 30))
        
        return {
            "score": round(score, 4),
            "ai_probability": round(float(normalized_ai_prob), 3),
            "is_ai": score < threshold
        }
