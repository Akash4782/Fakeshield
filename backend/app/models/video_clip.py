import torch
import torch.nn.functional as F
from transformers import CLIPProcessor, CLIPModel, SiglipProcessor, SiglipModel
from PIL import Image
import numpy as np
from app.models.loader_sync import MODEL_LOAD_LOCK

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# Pre-calibrate prompts for video deepfake detection
REAL_PROMPTS = [
    "a frame from a real video recorded by a camera",
    "natural video footage with authentic lighting",
    "a video clip from a real life camera",
]
AI_PROMPTS = [
    "a frame from an AI-generated synthetic video",
    "synthetic video contents from Sora, Runway, or Pika",
    "artificial textures and motion from a video generator",
]

class VideoClipModule:
    """Uses CLIP and SigLIP for zero-shot frame-level anomaly detection"""
    
    def __init__(self):
        print(f"[VideoClip] Initializing models on {DEVICE}...", flush=True)
        with MODEL_LOAD_LOCK:
            self.clip_model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32", low_cpu_mem_usage=False, device_map=None).to(DEVICE).eval()
        self.clip_processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32", use_fast=True)
        
        with MODEL_LOAD_LOCK:
            self.siglip_model = SiglipModel.from_pretrained("google/siglip-base-patch16-224", low_cpu_mem_usage=False, device_map=None).to(DEVICE).eval()
        self.siglip_processor = SiglipProcessor.from_pretrained("google/siglip-base-patch16-224", use_fast=True)

    @torch.no_grad()
    def analyze_frames(self, pil_frames: list) -> list:
        """Returns per-frame AI probability scores using ensemble of CLIP+SigLIP"""
        if not pil_frames: return []
        
        all_prompts = REAL_PROMPTS + AI_PROMPTS
        results = []
        
        for frame in pil_frames:
            # 1. CLIP Inference
            clip_inputs = self.clip_processor(text=all_prompts, images=frame, return_tensors="pt", padding=True).to(DEVICE)
            clip_outputs = self.clip_model(**clip_inputs)
            clip_probs = clip_outputs.logits_per_image.softmax(dim=1)[0].cpu().numpy()
            
            # 2. SigLIP Inference
            siglip_inputs = self.siglip_processor(text=all_prompts, images=frame, return_tensors="pt", padding=True).to(DEVICE)
            siglip_outputs = self.siglip_model(**siglip_inputs)
            siglip_probs = siglip_outputs.logits_per_image.softmax(dim=1)[0].cpu().numpy()
            
            # Aggregate AI probability (sum of AI prompts / total)
            clip_ai = clip_probs[len(REAL_PROMPTS):].sum()
            siglip_ai = siglip_probs[len(REAL_PROMPTS):].sum()
            
            # Ensemble (Mean)
            ensemble_ai = (clip_ai * 0.4 + siglip_ai * 0.6)
            results.append(float(ensemble_ai))
            
        return results

    def get_signal(self, pil_frames: list) -> dict:
        """Video-level spatial signal with timeline"""
        scores = self.analyze_frames(pil_frames)
        if not scores: return {"score": 0.5, "timeline": []}
        
        # Video level: 75th percentile to capture 'suspicious' regions rather than mean
        video_score = np.percentile(scores, 75)
        
        return {
            "score": float(video_score),
            "timeline": scores,
            "max_spike": float(max(scores))
        }
