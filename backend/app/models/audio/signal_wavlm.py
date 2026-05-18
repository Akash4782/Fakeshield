# signal_wavlm.py
"""
Signal 1b: WavLM-based SSL deepfake detection.

Model: abhishtagatya/wavlm-base-960h-itw-deepfake
(Fine-tuned for in-the-wild deepfakes, superior in noise/compression).

This is the new primary signal for Audio Lab v1.0.
"""

import torch
import torch.nn.functional as F
import numpy as np
import os
import threading
from transformers import (
    AutoFeatureExtractor,
    AutoModelForAudioClassification,
)
from app.models.loader_sync import MODEL_LOAD_LOCK

_model = None
_processor = None
_ai_label_idx = None
_load_lock = threading.Lock()
TARGET_SR = 16000


def _load_model():
    global _model, _processor, _ai_label_idx
    with _load_lock:
        if _model is not None:
            return

        # Industry-level WavLM model for in-the-wild (ITW) deepfakes
        model_id = "abhishtagatya/wavlm-base-960h-itw-deepfake"

        token = os.getenv("HF_TOKEN")
        try:
            print(f"Loading {model_id} (CPU Optimized)...")
            _processor = AutoFeatureExtractor.from_pretrained(model_id, token=token)
            # Use low_cpu_mem_usage=False to ensure NO "meta" device weights
            with MODEL_LOAD_LOCK:
                _model = (
                    AutoModelForAudioClassification.from_pretrained(
                        model_id, token=token, low_cpu_mem_usage=False, device_map=None
                    )
                    .to("cpu")
                    .eval()
                )
            _ai_label_idx = _detect_ai_label_index()
            print(f"[OK] WavLM loaded on CPU. AI label index: {_ai_label_idx}")
        except Exception as e:
            print(f"WavLM loading failed: {e}. Falling back to Wav2Vec2 in pipeline.")
            _model = None


def _detect_ai_label_index() -> int:
    """Detect which index = 'fake'."""
    if hasattr(_model.config, "id2label"):
        labels = _model.config.id2label
        for idx, label in labels.items():
            l = label.lower()
            if (
                any(k in l for k in ["fake", "spoof", "synthetic"])
                and "bonafide" not in l
            ):
                return int(idx)
        # If not found, check for real/bonafide and take the other
        for idx, label in labels.items():
            l = label.lower()
            if "bonafide" in l or "real" in l:
                return 1 - int(idx)  # binary assumption
    return 1  # default


def signal_wavlm(chunks: list[np.ndarray]) -> dict:
    """
    Run WavLM classifier on audio chunks.
    """
    _load_model()

    if _model is None or not chunks:
        return {
            "score": 0.5,
            "detail": {"reason": "model_unavailable"},
            "per_chunk": [],
        }

    chunk_scores = []
    try:
        # Pytorch Tensor Batching (5x-10x speedup over serial indexing)
        batch_in = [chunk[: TARGET_SR * 10] for chunk in chunks]

        inputs = _processor(
            batch_in,
            sampling_rate=TARGET_SR,
            return_tensors="pt",
            padding=True,
        )

        with torch.no_grad():
            # Ensure tensors are on the same device as the model
            inputs = {k: v.to("cpu") for k, v in inputs.items()}
            logits = _model(**inputs).logits
            probs = F.softmax(logits, dim=-1)

        # Extract individual chunk probabilities from batched output
        for i in range(len(chunks)):
            raw = float(probs[i][_ai_label_idx].item())
            chunk_scores.append(raw)

    except Exception as e:
        print(f"WavLM batch inference failed: {e}")
        chunk_scores = [0.5] * len(chunks)

    arr = np.array(chunk_scores)

    return {
        "score": round(float(np.mean(arr)), 3),
        "per_chunk": [round(s, 3) for s in chunk_scores],
        "detail": {
            "max": round(float(np.max(arr)), 3),
            "var": round(float(np.var(arr)), 4),
            "model": "wavlm-itw",
        },
    }
