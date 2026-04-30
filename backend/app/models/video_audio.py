import whisper
import mediapipe as mp
import numpy as np
import cv2
import librosa
import os
from pathlib import Path
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import urllib.request
from app.models.loader_sync import MODEL_LOAD_LOCK

_whisper_model = None
_face_landmarker = None

def _load_whisper():
    global _whisper_model
    if _whisper_model is None:
        print("[AudioLab] Loading Whisper Model...")
        with MODEL_LOAD_LOCK:
            _whisper_model = whisper.load_model("base")
    return _whisper_model

def _ensure_model_exists():
    """Industrial Downloader for Mediapipe Tasks model"""
    target_dir = Path("pt_models")
    if not target_dir.exists():
        target_dir.mkdir(parents=True, exist_ok=True)
    
    file_path = target_dir / "face_landmarker.task"
    if not file_path.exists():
        url = "https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/1/face_landmarker.task"
        print(f"[FETCH] Downloading Lip-Sync model (~5.6MB) to {file_path}...")
        try:
            urllib.request.urlretrieve(url, str(file_path))
            print("[OK] Model downloaded successfully.")
        except Exception as e:
            print(f"[FAIL] Download failed: {e}. Lip-Sync may not work.")

def _load_face_mesh():
    """Migrated to Mediapipe Tasks FaceLandmarker"""
    _ensure_model_exists()
    global _face_landmarker
    if _face_landmarker is None:
        model_path = os.path.join("pt_models", "face_landmarker.task")
        if not os.path.exists(model_path):
            # Fallback path if run from different CWD
            model_path = os.path.join(os.path.dirname(__file__), "..", "..", "pt_models", "face_landmarker.task")
            
        base_options = python.BaseOptions(model_asset_path=model_path)
        options = vision.FaceLandmarkerOptions(
            base_options=base_options,
            output_face_blendshapes=False,
            output_facial_transformation_matrixes=False,
            num_faces=1
        )
        with MODEL_LOAD_LOCK:
            _face_landmarker = vision.FaceLandmarker.create_from_options(options)
    return _face_landmarker

# Lip landmark indices (Legacy indices still apply to Task mesh)
LIP_UPPER_IDX = [61, 185, 40, 39, 37, 0, 267, 269, 270, 409, 291]
LIP_LOWER_IDX = [146, 91, 181, 84, 17, 314, 405, 321, 375, 291]

class VideoAudioModule:
    """Detects Lip-Sync Mismatch using Whisper + Mediapipe Tasks"""
    
    def __init__(self):
        self.model = _load_whisper()
        self.detector = _load_face_mesh()

    def get_lip_openness(self, bgr_frame) -> float:
        """Returns normalized lip openness (0=closed, 1=open) using Tasks API"""
        rgb_frame = cv2.cvtColor(bgr_frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
        
        detection_result = self.detector.detect(mp_image)
        
        if not detection_result.face_landmarks:
            return -1.0 # No face
            
        landmarks = detection_result.face_landmarks[0]
        h, w = bgr_frame.shape[:2]
        
        upper_y = np.mean([landmarks[i].y * h for i in LIP_UPPER_IDX])
        lower_y = np.mean([landmarks[i].y * h for i in LIP_LOWER_IDX])
        
        # Face height for normalization (Forehead to Chin)
        face_height = abs(landmarks[10].y - landmarks[152].y) * h
        
        openness = abs(lower_y - upper_y) / (face_height + 1e-8)
        return float(openness)

    def analyze_audio_visual(self, audio_path: str, frames_bgr: list, fps: int) -> dict:
        """Compares Whisper-detected speech vs Lip openness timeline"""
        try:
            # 1. Whisper Transcription + Word Timestamps
            result = self.model.transcribe(audio_path, word_timestamps=True, fp16=False)
            segments = result.get("segments", [])
            
            # 2. Extract Lip Timeline
            lip_timeline = []
            for f in frames_bgr:
                lip_timeline.append(self.get_lip_openness(f))
            
            # 3. Synchronize
            audio_speaking = np.zeros(len(frames_bgr))
            for seg in segments:
                start_frame = int(seg['start'] * fps)
                end_frame   = int(seg['end'] * fps)
                audio_speaking[max(0, start_frame):min(len(frames_bgr), end_frame)] = 1.0
            
            # 4. Score Mismatch
            lip_active = np.array([1.0 if d > 0.02 else (0.0 if d >= 0 else np.nan) for d in lip_timeline])
            
            # Mask out frames without faces
            valid_mask = ~np.isnan(lip_active)
            if valid_mask.sum() < 3: 
                return {"score": 0.5, "mismatch_rate": 0.0, "reason": "No face detected"}
                
            # Agreement rate between lip motion and audio
            agreement = np.mean(lip_active[valid_mask] == audio_speaking[valid_mask])
            mismatch_rate = 1.0 - agreement
            
            # AI Probability: Mismatch is a strong signal for deepfakes
            ai_prob = min(max(mismatch_rate * 2.0, 0.0), 1.0)
            
            return {
                "score": float(ai_prob),
                "mismatch_rate": float(mismatch_rate),
                "lip_timeline": [float(d) for d in lip_timeline],
                "audio_speaking": [int(s) for s in audio_speaking.tolist()]
            }
        except Exception as e:
            print(f"[VideoAudio] Error: {e}")
            return {"score": 0.5, "error": str(e)}
