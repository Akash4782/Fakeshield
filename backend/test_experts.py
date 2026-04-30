import os
import torch
import numpy as np
import cv2
from PIL import Image

# Mock the signals
from app.services.video.spatial_vit import signal_spatial_vit
from app.services.video.temporal_videomae import signal_temporal_videomae
from app.services.video.multimodal_xclip import signal_multimodal_xclip
from app.services.video.physics_prnu import extract_noise_residual
from app.services.video.frame_sampler import extract_frames

def debug_expert(video_path, label):
    print(f"\n--- DEBUGGING [{label}] Video: {video_path} ---")
    bgr, _ = extract_frames(video_path, max_frames=16)
    pil = [Image.fromarray(cv2.cvtColor(f, cv2.COLOR_BGR2RGB)) for f in bgr]
    
    # 1. PRNU
    prnu = extract_noise_residual(bgr)
    print(f"PRNU: {prnu}")
    
    # 2. Spatial ViT
    vit = signal_spatial_vit(pil)
    print(f"ViT: {vit}")
    
    # 3. Temporal
    mae = signal_temporal_videomae(pil)
    print(f"MAE: {mae}")
    
    # 4. X-CLIP
    xclip = signal_multimodal_xclip(pil)
    print(f"X-CLIP: {xclip}")

if __name__ == "__main__":
    ai_video = "test_data/dataset/ai_10/ai_1.mp4"
    debug_expert(ai_video, "AI")
