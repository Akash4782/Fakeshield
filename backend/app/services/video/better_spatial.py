# better_spatial.py  — v3  FIXED MODEL IDs
"""
Deepfake-specialist spatial ensemble on face crops.

FIXED vs v2:
  - Removed non-existent model "xceptionnet/deepfake-detection-swin"
  - Both models are verified on HuggingFace as of 2025
  - Dynamic label detection — no hardcoded indices
  - Handles None images (frames with no detected face) cleanly

Model A:  prithivMLmods/AI-vs-Deepfake-vs-Real-Siglip2
          3-class (AI / Deepfake / Real). SigLIP2 backbone.
          Catches both AIGC images AND face-swap deepfakes.

Model B:  prithivMLmods/Deep-Fake-Detector-v2-Model
          Binary (Deepfake / Realism). ViT backbone. DFDC-trained.
          Strong on face-swap deepfakes.

Ensemble: Model A weighted 0.55, Model B weighted 0.45.
          When models disagree > 0.30 → pull toward 0.5 (uncertainty).
"""

import torch
import torch.nn.functional as F
import numpy as np
from PIL import Image
from transformers import AutoImageProcessor

# Monkey patch for optimum compatibility with new transformers
import transformers.utils

if not hasattr(transformers.utils, "is_offline_mode"):
    transformers.utils.is_offline_mode = lambda: False

import transformers.generation

if not hasattr(transformers.generation, "GenerationMixin"):

    class GenerationMixin:
        pass

    transformers.generation.GenerationMixin = GenerationMixin

from optimum.onnxruntime import ORTModelForImageClassification
import torch.nn.functional as F
from app.models.loader_sync import MODEL_LOAD_LOCK

# Global model cache — loaded once, reused
_models: dict = {}

# ─────────────────────────────────────────────────────────────────────────────
#  MODEL CONFIG
# ─────────────────────────────────────────────────────────────────────────────

_MODEL_CONFIGS = [
    {
        "key": "siglip2",
        "id": "prithivMLmods/AI-vs-Deepfake-vs-Real-Siglip2",
        "weight": 0.55,
        "is_onnx": False,
        "processor_class": "SiglipImageProcessor",
        "fake_keywords": ["ai", "fake", "deepfake", "generated", "synthetic"],
    },
    {
        "key": "vit_dfdc",
        "id": "onnx-community/Deep-Fake-Detector-v2-Model-ONNX",
        "weight": 0.45,
        "is_onnx": True,
        "processor_class": "ViTImageProcessor",
        "fake_keywords": ["deepfake", "fake", "ai", "generated"],
    },
]


# ─────────────────────────────────────────────────────────────────────────────
#  LOADER
# ─────────────────────────────────────────────────────────────────────────────


def warm_up_spatial_models():
    """Warms up models at startup to prevent latency spikes during first request."""
    global _models
    if _models:
        return

    total = len(_MODEL_CONFIGS)
    for i, cfg in enumerate(_MODEL_CONFIGS, 1):
        key = cfg["key"]
        hf_id = cfg["id"]
        try:
            print(f"      [{i}/{total}] Loading {key} ({'ONNX' if cfg['is_onnx'] else 'PT'}): {hf_id}...")
            #  Cleaner Loading Logic — Bypassing AutoImageProcessor mapping failures
            from transformers import SiglipImageProcessor, ViTImageProcessor, AutoImageProcessor
            
            p_class_name = cfg.get("processor_class")
            try:
                if p_class_name == "SiglipImageProcessor":
                    processor = SiglipImageProcessor.from_pretrained(hf_id)
                elif p_class_name == "ViTImageProcessor":
                    processor = ViTImageProcessor.from_pretrained(hf_id)
                else:
                    processor = AutoImageProcessor.from_pretrained(hf_id, use_fast=True)
            except Exception as e:
                # Last resort fallback if explicit class fails
                print(f"      [WARN] Direct loading failed for {key}, attempting Auto fallback: {e}")
                processor = AutoImageProcessor.from_pretrained(hf_id, use_fast=True)
            
            if cfg["is_onnx"]:
                try:
                    with MODEL_LOAD_LOCK:
                        from transformers import AutoConfig
                        config = AutoConfig.from_pretrained(hf_id)
                        model = ORTModelForImageClassification.from_pretrained(
                            hf_id, 
                            provider="CPUExecutionProvider",
                            subfolder="onnx",
                            file_name="model.onnx",
                            config=config
                        )
                except Exception as e:
                    print(f"      [WARN] Could not load ONNX model {hf_id}. Error: {e}", flush=True)
                    raise e
                device = torch.device("cpu")
            else:
                from transformers import AutoModelForImageClassification
                device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
                with MODEL_LOAD_LOCK:
                    model = AutoModelForImageClassification.from_pretrained(
                        hf_id, low_cpu_mem_usage=False, device_map=None
                    ).to(device)
                model.eval()

            fake_indices = _find_fake_indices(model, cfg["fake_keywords"])
            _models[key] = {
                "model": model,
                "processor": processor,
                "fake_indices": fake_indices,
                "weight": cfg["weight"],
                "id": hf_id,
                "device": device,
                "is_onnx": cfg["is_onnx"],
            }
            print(f"         [OK] {key} initialized on {device}")
        except Exception as e:
            print(f"     [FAIL] Failed to load {hf_id}: {e}")


def _find_fake_indices(model, fake_keywords: list[str]) -> list[int]:
    """
    Inspect model.config.id2label and return all indices whose label
    matches any keyword in fake_keywords (case-insensitive).
    Falls back to [1] if nothing matches (standard binary convention).
    """
    id2label: dict = getattr(model.config, "id2label", {})
    indices = []
    for idx, label in id2label.items():
        label_lower = label.lower()
        if any(kw in label_lower for kw in fake_keywords):
            indices.append(int(idx))
    if not indices:
        indices = [1]  # Binary model convention: 0=real, 1=fake
    return indices


# ─────────────────────────────────────────────────────────────────────────────
#  INFERENCE
# ─────────────────────────────────────────────────────────────────────────────


@torch.no_grad()
def _run_model_on_batch(
    key: str,
    pil_images: list[Image.Image],
) -> list[float]:
    """
    Run one model over a batch of PIL images.
    Returns list of fake-probability floats in [0, 1].
    """
    m = _models[key]
    model = m["model"]
    processor = m["processor"]
    fake_idx = m["fake_indices"]

    # 1. Process images to tensors
    inputs = processor(images=pil_images, return_tensors="pt")

    # 2. Move to device (only for PyTorch, ONNX handles its own execution)
    if not m.get("is_onnx"):
        device = m["device"]
        inputs = {k: v.to(device) for k, v in inputs.items()}

    # 3. Inference
    outputs = model(**inputs)
    logits = outputs.logits

    # 4. Handle output (convert to torch if it's a numpy array from ONNX)
    if isinstance(logits, np.ndarray):
        logits = torch.from_numpy(logits)

    probs = F.softmax(logits, dim=-1)  # [B, n_classes]
    fake_probs = probs[:, fake_idx].sum(dim=-1)  # [B]
    return fake_probs.tolist()


def _amplify(score: float, power: float = 0.75) -> float:
    """
    Soft amplification: pulls scores away from 0.5 toward extremes.
    Reduces wishy-washy 0.48–0.52 outputs from uncertain frames.
    """
    s = max(0.0, min(1.0, score))
    if s > 0.5:
        return 0.5 + 0.5 * (((s - 0.5) / 0.5) ** power)
    return 0.5 - 0.5 * (((0.5 - s) / 0.5) ** power)


# ─────────────────────────────────────────────────────────────────────────────
#  PUBLIC API
# ─────────────────────────────────────────────────────────────────────────────


def signal_spatial_ensemble_batch(
    pil_images: list,  # list[Optional[PIL.Image.Image]]
    use_faces: bool = True,
) -> dict:
    """
    Run 2-model deepfake-specialist ensemble on a batch of images.

    Args:
        pil_images:  Face crops (preferred) or full frames. None = no face.
        use_faces:   Whether these are face crops (for reporting).

    Returns:
        score:   0–1 AI probability (higher = more likely AI/deepfake)
        detail:  Per-model breakdown + per-frame scores.
    """
    warm_up_spatial_models()

    if not _models:
        return {"score": 0.5, "detail": {"reason": "no spatial models loaded"}}

    # Filter None (frames with no face detected)
    valid = [(i, img) for i, img in enumerate(pil_images) if img is not None]
    if not valid:
        return {"score": 0.5, "detail": {"reason": "no valid images to score"}}

    valid_imgs = [img for _, img in valid]

    # Run each model
    per_model_scores: dict[str, list[float]] = {}
    for key in _models:
        try:
            scores = _run_model_on_batch(key, valid_imgs)
            per_model_scores[key] = scores
        except Exception as e:
            print(f"  ⚠️  Spatial model {key} inference error: {e}")
            per_model_scores[key] = [0.5] * len(valid_imgs)

    # Ensemble: weighted combination per frame
    frame_scores = []
    total_weight = sum(m["weight"] for m in _models.values())

    for i in range(len(valid_imgs)):
        model_scores = {k: per_model_scores[k][i] for k in _models}

        # Disagreement check
        scores_arr = list(model_scores.values())
        if len(scores_arr) >= 2:
            disagreement = max(scores_arr) - min(scores_arr)
        else:
            disagreement = 0.0

        if disagreement > 0.30:
            # Models disagree: average but pull toward 0.5
            raw = sum(scores_arr) / len(scores_arr)
            fused = raw * 0.82 + 0.5 * 0.18  # uncertainty penalty
        else:
            # Weighted average
            fused = (
                sum(_models[k]["weight"] * model_scores[k] for k in _models)
                / total_weight
            )

        frame_scores.append(_amplify(fused))

    arr = np.array(frame_scores)

    return {
        "score": float(np.mean(arr)),
        "detail": {
            "frames_analyzed": len(valid_imgs),
            "face_analysis": use_faces,
            "ensemble_mean": round(float(np.mean(arr)), 3),
            "ensemble_max": round(float(np.max(arr)), 3),
            "ensemble_min": round(float(np.min(arr)), 3),
            "ensemble_variance": round(float(np.var(arr)), 4),
            "per_frame_scores": [round(s, 3) for s in frame_scores],
            **{
                f"{k}_mean": round(float(np.mean(per_model_scores[k])), 3)
                for k in per_model_scores
            },
            "models_loaded": list(_models.keys()),
        },
    }
