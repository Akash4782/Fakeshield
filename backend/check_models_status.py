import os
import sys
import torch

# Add backend to path
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "app")))
sys.path.append(os.getcwd())

from app.models.image_detector import load_image_models
import app.models.image_detector as idet

print("Initial status:")
print(f"S1_LOADED: {idet.S1_LOADED}")
print(f"S2_LOADED: {idet.S2_LOADED}")
print(f"CLIP_LOADED: {idet.CLIP_LOADED}")
print(f"_DINO_MODEL: {idet._DINO_MODEL is not None}")

print("\nLoading models...")
load_image_models()

print("\nPost-load status:")
print(f"S1_LOADED: {idet.S1_LOADED}")
print(f"S2_LOADED: {idet.S2_LOADED}")
print(f"CLIP_LOADED: {idet.CLIP_LOADED}")
print(f"_DINO_MODEL: {idet._DINO_MODEL is not None}")

if idet.S1_LOADED and idet.S1_MODEL is not None:
    print(f"S1 Model Device: {next(idet.S1_MODEL.parameters()).device}")
if idet.CLIP_LOADED and idet.CLIP_MODEL is not None:
    print(f"CLIP Model Device: {next(idet.CLIP_MODEL.parameters()).device}")
