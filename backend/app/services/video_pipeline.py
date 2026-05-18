import time
import asyncio
import os
from typing import List, Dict, Any
import numpy as np
from PIL import Image
import concurrent.futures
from app.services.video.video_metadata import VideoMetadataForensics

# Forensic module imports moved inside get_video_modules() for lazy loading
_video_modules = {}

def get_video_module(name: str):
    """Refined lazy loader: Only initializes the requested forensic module."""
    global _video_modules
    if name in _video_modules:
        return _video_modules[name]

    print(f"[v11.0-Lazy] Initializing module: '{name}'...", flush=True)
    
    # Mapping of keys to their respective loader classes
    loaders = {
        "sampler":   lambda: __import__("app.services.video_sampler", fromlist=["VideoSampler"]).VideoSampler,
        "clip":      lambda: __import__("app.models.video_clip", fromlist=["VideoClipModule"]).VideoClipModule,
        "audio":     lambda: __import__("app.models.video_audio", fromlist=["VideoAudioModule"]).VideoAudioModule,
        "tempo":     lambda: __import__("app.models.video_tempo_raft", fromlist=["VideoTempoRaft"]).VideoTempoRaft,
        "forensic":  lambda: __import__("app.models.video_forensics_v2", fromlist=["VideoForensicsV2"]).VideoForensicsV2,
        "reasoning": lambda: __import__("app.models.video_reasoning", fromlist=["VideoReasoningModule"]).VideoReasoningModule,
        "fusion":    lambda: __import__("app.models.video_fusion", fromlist=["VideoFusionEngine"]).VideoFusionEngine,
        "metadata":  lambda: __import__("app.services.video.video_metadata", fromlist=["VideoMetadataForensics"]).VideoMetadataForensics
    }

    if name not in loaders:
        raise ValueError(f"Unknown video module: {name}")

    try:
        loader_cls = loaders[name]()
        _video_modules[name] = loader_cls()
        print(f"  [OK] Module '{name}' is ready.", flush=True)
        return _video_modules[name]
    except Exception as e:
        print(f"  [FAIL] Failed to load module '{name}': {e}", flush=True)
        raise e

def get_video_modules():
    """Backward compatibility singleton loader."""
    # This is used by the startup warm-up sequence to pre-load models in background.
    # We'll just return a proxy that loads on demand.
    class ModuleProxy:
        def __getitem__(self, name: str):
            return get_video_module(name)
    return ModuleProxy()

async def run_video_pipeline_v10(video_path: str) -> Dict[str, Any]:
    """
    V11.0 'Perfect Phased Pipeline' Architecture - Optimized for Speed
    Phases:
      1. Signal (Metadata, C2PA, Fast Watermark) -> Short Circuit (<1s)
      2. Technical Audit (FFT, Noise, Physics) -> Short Circuit (<3s)
      3. Deep Ensembles (Deep Video Models, Audio-Visual) -> Fallback (~5-15s)
    """
    mods = get_video_modules()
    sampler = mods["sampler"]
    fusion_engine = mods["fusion"]
    meta_scanner = mods["metadata"]

    start_time = time.time()
    
    # ── PHASE 1: DIRECT AI SIGNATURE CHECK (QUICK PASS) ────────────────────────
    print(f"[v11.0-P1] Scanning Signatures: {video_path}")
    
    # 1a. Container Metadata Scan
    container_meta = meta_scanner.get_metadata(video_path)
    if container_meta["ai_score"] > 0.90:
        print(f"  [P1-HIT] AI Metadata markers found.")
        elapsed = round(time.time() - start_time, 2)
        return _assemble_short_circuit("Phase 1: Metadata", container_meta["ai_score"], [f"AI Marker in container: {m}" for m in container_meta["markers"]], container_meta, elapsed)

    # 1b. C2PA Check
    c2pa_res = meta_scanner.check_c2pa(video_path)
    if c2pa_res.get("has_c2pa") and c2pa_res.get("is_ai"):
        print(f"  [P1-HIT] C2PA Manifest confirms AI.")
        elapsed = round(time.time() - start_time, 2)
        return _assemble_short_circuit("Phase 1: C2PA", 1.0, ["Content Credentials confirm AI origin."], container_meta, elapsed)

    # 1c. Fast Visual Scan (Watermark on first frame)
    # Lazy load ONLY the first frame for the quick pass
    _, p1_frames_pil = sampler.extract_frames(video_path, count=1, 특정_indices=[0])
    if p1_frames_pil:
        from app.models.image_detector import sig_gemini_watermark
        is_gemini, gemini_vis = sig_gemini_watermark(p1_frames_pil[0])
        if is_gemini:
            print(f"  [P1-HIT] Gemini Watermark detected on first frame.")
            elapsed = round(time.time() - start_time, 2)
            return _assemble_short_circuit("Phase 1: Watermark", 0.99, ["Google Gemini 'Sparkle' watermark identified."], container_meta, elapsed, evidence_vis=gemini_vis)

    # ── PHASE 2: TECHNICAL FORENSIC AUDIT ──────────────────────────────────────
    print(f"[v11.0-P2] Forensic Audit (FFT/Physics/Noise Residuals)...")
    # Lazy load the full 8 frames for technical analysis
    frames_np, frames_pil = sampler.extract_frames(video_path, count=8)
    if not frames_np:
        return {"status": "error", "detail": "Sampling failed"}
    
    meta = sampler.get_info(video_path)
    full_meta = {**meta, **container_meta}
    
    forensics_v2 = mods["forensic"]
    reasoning_module = mods["reasoning"]
    
    # Fast Technical Signals
    f2_signal = forensics_v2.get_signal(frames_np)
    
    if f2_signal["score"] > 0.94:
        print(f"  [P2-HIT] FFT/Noise anomaly detected (Fast).")
        elapsed = round(time.time() - start_time, 2)
        return _assemble_short_circuit("Phase 2: Technical (FFT)", f2_signal["score"], ["Extreme spectral anomaly (Periodic AI noise)."], full_meta, elapsed)
    # ── PHASE 3: DEEP ENSEMBLES (FALLBACK NEURAL ANALYSIS) ──────────────────────
    print(f"[v11.0-P3] Falling back to Deep AI Video Models (Parallel Ensemble)...")
    clip_module = mods["clip"]
    audio_module = mods["audio"]
    tempo_raft = mods["tempo"]
    
    # Lazy Audio Extraction (only if we reach Phase 3)
    audio_path = sampler.extract_audio(video_path)
    fps = meta.get("fps", 2)
    
    # Subsample frames for deep models to cut processing time in half
    frames_pil_deep = frames_pil[::2]
    frames_np_deep = frames_np[::2]
    
    # CPU Optimization: Limit PyTorch threads to 1 to prevent core-contention thrashing on Hugging Face Space vCPUs.
    # Sequential execution prevents severe OOMs and CPU locks under tight resources.
    import torch
    torch.set_num_threads(1)
    
    print("[v11.0-P3] Executing Spatial Deep Ensemble (SigLIP)...", flush=True)
    res_spatial = clip_module.get_signal(frames_pil_deep)
    
    print("[v11.0-P3] Executing Temporal Optical Flow (RAFT)...", flush=True)
    res_temporal = tempo_raft.get_signal(frames_np_deep)
    
    print("[v11.0-P3] Executing Audio-Visual Lip-Sync (Whisper)...", flush=True)
    res_audio = audio_module.analyze_audio_visual(audio_path, frames_np, fps)
    
    print("[v11.0-P3] Executing Visual Physics Reasoning (Moondream)...", flush=True)
    res_reasoning = reasoning_module.analyze_physics(frames_pil_deep)
    
    signals_map = {
        "spatial": res_spatial.get("score", 0.5),
        "temporal": res_temporal.get("score", 0.5),
        "audio": res_audio.get("score", 0.5),
        "forensic": f2_signal.get("score", 0.5),
        "reasoning": res_reasoning.get("score", 0.5)
    }
    
    report = fusion_engine.fuse_signals(signals_map, metadata=full_meta)
    
    processing_time = round(time.time() - start_time, 2)
    return {
        "status": "success",
        "data": {
            **report,
            "metadata": full_meta,
            "processing_time": f"{processing_time}s",
            "engine_version": "v11.0-PhasedOptimized",
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "evidence_heatmap": res_temporal.get("evidence_heatmap"),
            "timelines": {
                "spatial": res_spatial.get("timeline", []),
                "temporal": res_temporal.get("mag_timeline", []),
                "audio_lip": res_audio.get("lip_timeline", []),
                "audio_speaking": res_audio.get("audio_speaking", []),
                "forensic_fft": f2_signal.get("fft_score", 0.5)
            },
            "reasoning_report": res_reasoning.get("reasoning", "")
        }
    }

def _assemble_short_circuit(phase_name, prob, reasons, meta, elapsed, evidence_vis=None):
    """Utility to format a short-circuited response."""
    import time
    verdict = "DEEPFAKE" if prob >= 0.75 else "UNCERTAIN"
    threat = "CRITICAL" if prob >= 0.75 else "MEDIUM"
    
    return {
        "status": "success",
        "data": {
            "verdict": verdict,
            "threat_level": threat,
            "ai_probability": prob,
            "confidence": round(prob * 100, 1),
            "reasons": [f"✗ [{phase_name}] {r}" for r in reasons],
            "metadata": meta,
            "processing_time": f"{elapsed}s",
            "engine_version": f"v11.0-PerfectPhased (ShortCircuit)",
            "evidence_heatmap": evidence_vis,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "signals": {"phase_hit": prob},
            "logic_version": "v11.0-ShortCircuit",
            "timelines": { "spatial": [], "temporal": [], "audio_lip": [], "audio_speaking": [] },
            "reasoning_report": "Direct provenance hit. Physical consistency check skipped for speed."
        }
    }
