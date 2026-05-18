import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, GenerationMixin, GenerationConfig
from PIL import Image
import numpy as np
from app.models.loader_sync import MODEL_LOAD_LOCK

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# Monkeypatch Cache and DynamicCache to restore deprecated get_usable_length method in newer transformers.
# This prevents 'DynamicCache' attribute crashes in older model remote files under transformers 4.45+.
try:
    from transformers.cache_utils import Cache, DynamicCache
    
    def get_usable_length_patch(self, *args, **kwargs):
        layer_idx = 0
        if len(args) > 1:
            layer_idx = args[1]
        elif "layer_idx" in kwargs:
            layer_idx = kwargs["layer_idx"]

        if hasattr(self, "get_seq_length"):
            return self.get_seq_length(layer_idx)
        if hasattr(self, "seen_tokens"):
            return self.seen_tokens
        if hasattr(self, "key_cache") and len(self.key_cache) > layer_idx:
            k = self.key_cache[layer_idx]
            if hasattr(k, "shape"):
                return k.shape[-2]
        return 0

    Cache.get_usable_length = get_usable_length_patch
    DynamicCache.get_usable_length = get_usable_length_patch
    print("[VideoReasoning] Successfully monkeypatched Cache.get_usable_length for transformers 4.45+ compatibility.", flush=True)
except Exception as e:
    print(f"[VideoReasoning] Cache monkeypatch warning: {e}", flush=True)

class VideoReasoningModule:
    """Uses Moondream2 (VLM) for visual consistency reasoning"""
    
    def __init__(self):
        print(f"[VideoReasoning] Loading Moondream2 on {DEVICE}...")
        self.model_id = "vikhyatk/moondream2"
        self.revision = "2024-08-26"
        with MODEL_LOAD_LOCK:
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_id, 
                trust_remote_code=True, 
                revision=self.revision,
                low_cpu_mem_usage=False,
                device_map=None
            ).to(DEVICE).eval()

        # Disable KV Cache to avoid 'DynamicCache' compat issues with newer transformers packages
        self.model.config.use_cache = False
        if hasattr(self.model, "text_model") and self.model.text_model is not None:
            if hasattr(self.model.text_model, "config") and self.model.text_model.config is not None:
                self.model.text_model.config.use_cache = False

        # Explicitly initialize generation config for transformers 4.45+ compatibility
        # This prevents the "'NoneType' object has no attribute '_from_model_config'" error
        try:
            self.model.generation_config = GenerationConfig.from_model_config(self.model.config)
            # Moondream2 often wraps a Phi sub-model; propagate the config to avoid child-level generation errors
            if hasattr(self.model, "model") and self.model.model is not None:
                self.model.model.generation_config = self.model.generation_config
        except Exception as e:
            print(f"[VideoReasoning] GenerationConfig Warning: {e}")
        
        # Recursive patch for transformers 4.50+ compatibility
        # PhiForCausalLM no longer inherits from GenerationMixin in newer transformers,
        # but moondream2's remote code expects .generate() to be available on sub-models.
        def patch_recursive(m, path="model"):
            if m.__class__.__name__ == "PhiForCausalLM" or (
                not hasattr(m, "generate") and hasattr(m, "prepare_inputs_for_generation")
            ):
                if not isinstance(m, GenerationMixin):
                    print(f"[VideoReasoning] Patching {path} ({m.__class__.__name__}) with GenerationMixin...")
                    m.__class__ = type(
                        m.__class__.__name__, 
                        (m.__class__, GenerationMixin), 
                        {}
                    )
                # Propagate valid generation config to prevent child-level config lookup exceptions
                try:
                    m.generation_config = self.model.generation_config
                except Exception:
                    pass
            
            for name, child in m.named_children():
                patch_recursive(child, f"{path}.{name}")

        patch_recursive(self.model)

        # Enforce use_cache=False dynamically on both generation layers to bypass DynamicCache instantiation
        try:
            if hasattr(self.model, "text_model") and self.model.text_model is not None:
                orig_text_gen = self.model.text_model.generate
                def patched_text_gen(*args, **kwargs):
                    kwargs["use_cache"] = False
                    return orig_text_gen(*args, **kwargs)
                self.model.text_model.generate = patched_text_gen
        except Exception as e:
            print(f"[VideoReasoning] Text model generate patch warning: {e}", flush=True)

        try:
            orig_model_gen = self.model.generate
            def patched_model_gen(*args, **kwargs):
                kwargs["use_cache"] = False
                return orig_model_gen(*args, **kwargs)
            self.model.generate = patched_model_gen
        except Exception as e:
            print(f"[VideoReasoning] Model generate patch warning: {e}", flush=True)
        
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_id, revision=self.revision, use_fast=True)

    def ask(self, pil_image: Image.Image, question: str) -> str:
        """Asks a question about a frame-level physics inconsistency"""
        try:
            enc_image = self.model.encode_image(pil_image)
            answer = self.model.answer_question(enc_image, question, self.tokenizer, use_cache=False, max_new_tokens=30)
            return answer.strip()
        except Exception as e:
            print(f"[VideoReasoning] Ask Error: {e}")
            return "Unable to reason about this frame."

    def analyze_physics(self, frames_pil: list) -> dict:
        """
        V11.0 CPU Optimized: Compressed Forensic Reasoning
        Reduces 3 inference passes to 1 structured pass.
        """
        if not frames_pil: return {"score": 0.5, "reasoning": "No frames provided for reasoning."}
        
        target_idx = len(frames_pil) // 2
        target_frame = frames_pil[target_idx]
        
        # Consolidated Forensic Prompt - Optimized strictly for < 15 words to prevent LLM hanging
        question = (
            "Analyze this frame for AI anomalies (warping, shadows, blurring). "
            "Keep response strictly under 15 words. "
            "End with exactly 'CONSISTENT' or 'INCONSISTENT'."
        )
        
        try:
            obs = self.ask(target_frame, question)
            lower_obs = obs.lower()
            
            # Weighted Keyword Analysis for CPU-friendly scoring
            suspicious_terms = ["warp", "merge", "ghost", "inconsistent", "unnatural", "blur", "morph", "artificial", "maybe", "not match"]
            safe_terms = ["consistent", "natural", "clear", "matched", "perfect", "logical", "realistic"]
            
            score = 0.45 # Neutral/Safe baseline
            
            # Count suspicious indicators
            hit_count = sum(1 for term in suspicious_terms if term in lower_obs)
            safe_count = sum(1 for term in safe_terms if term in lower_obs)
            
            if "inconsistent" in lower_obs or hit_count >= 2:
                score = 0.85
            elif hit_count == 1:
                score = 0.65
            elif "consistent" in lower_obs and hit_count == 0:
                score = 0.15
            
            return {
                "score": float(np.clip(score, 0.1, 0.9)),
                "reasoning": f"FORENSIC_SUMMARY: {obs}"
            }
        except Exception as e:
            print(f"[VideoReasoning] Optimized pass failed: {e}")
            return {"score": 0.5, "reasoning": "Reasoning engine failure."}
