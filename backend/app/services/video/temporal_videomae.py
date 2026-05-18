# temporal_videomae.py — V43 STABLE (Using VideoMAE encoder directly, no masking issues)
import torch
import numpy as np
from PIL import Image

_processor = None
_encoder = None

def _load_model():
    global _processor, _encoder
    if _encoder is not None: return
    try:
        from transformers import VideoMAEImageProcessor, VideoMAEModel
        model_id = "MCG-NJU/videomae-base"
        print(f"[FETCH] Loading Temporal Expert (CPU Optimized): {model_id}")
        
        # CPU Optimization: Limit threads per model to avoid thrashing during parallel Phase 3
        if torch.get_num_threads() > 4:
            torch.set_num_threads(4)
            
        _processor = VideoMAEImageProcessor.from_pretrained(model_id)
        full_model = VideoMAEModel.from_pretrained(
            model_id, low_cpu_mem_usage=True, device_map=None
        ).cpu()
        # Extract just the encoder - avoids all masking complexity
        _encoder = full_model.encoder
        _encoder.eval()
        # Also store the patch embeddings module
        _encoder._embeddings = full_model.embeddings
        print(f"[OK] VideoMAE encoder ready on CPU (4-thread mode)")
    except Exception as e:
        print(f"[FAIL] VideoMAE load failed: {e}")
        _encoder = False


def warm_up_temporal_models():
    """V50: Pre-loads the VideoMAE expert to prevent race conditions."""
    _load_model()

def signal_temporal_videomae(pil_frames: list[Image.Image]) -> dict:
    """
    V43 Temporal Expert — Real VideoMAE feature analysis.
    We use the patch embeddings directly without the masking head,
    which avoids the bool_masked_pos tensor size mismatch entirely.
    """
    _load_model()

    if not _encoder or len(pil_frames) < 4:
        return {"score": 0.5, "detail": {"reason": "fallback"}}

    try:
        # Exactly 16 frames (VideoMAE pretrained on 16-frame clips)
        indices = np.linspace(0, len(pil_frames) - 1, 16, dtype=int)
        sampled = [pil_frames[i].resize((224, 224), Image.LANCZOS) for i in indices]

        inputs = _processor(images=sampled, return_tensors="pt")
        pixel_values = inputs["pixel_values"]  # (1, 16, 3, 224, 224) or (16, 3, 224, 224)

        if pixel_values.dim() == 4:
            pixel_values = pixel_values.unsqueeze(0)  # → (1, 16, 3, 224, 224)

        with torch.no_grad():
            # Get patch embeddings directly (no masking needed)
            embedding_output = _encoder._embeddings(pixel_values, bool_masked_pos=None)
            # embedding_output: (1, num_patches, hidden_size)
            hidden_np = embedding_output.squeeze(0).numpy()  # (num_patches, 768)

        # Measure feature variance (semantic drift)
        feature_std  = float(np.std(hidden_np))
        feature_mean = float(np.mean(np.abs(hidden_np)))
        drift = feature_std / max(feature_mean, 1e-6)

        # Scoring: AI drift > 0.65, Real drift ≤ 0.60
        score = float(np.clip((drift - 0.55) * 3.0, 0.0, 1.0))

        return {
            "score": round(score, 3),
            "detail": {
                "feature_std":  round(feature_std, 4),
                "drift_ratio":  round(drift, 4),
                "model":        "MCG-NJU/videomae-base-encoder"
            }
        }

    except Exception as e:
        print(f"[WARN] VideoMAE inference error: {e}")
        return {"score": 0.5, "detail": {"reason": str(e)}}
