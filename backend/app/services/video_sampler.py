import cv2
import numpy as np
from PIL import Image
import os
import subprocess
import tempfile

class VideoSampler:
    """Extracts frames and audio for forensic analysis with lazy-loading support."""
    
    def get_info(self, video_path: str):
        """Quickly probes video for meta information."""
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened(): return {}
        
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        duration = total_frames / (fps if fps > 0 else 1)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        cap.release()
        
        return {
            "duration": round(duration, 2),
            "fps": round(fps, 1),
            "total_frames": total_frames,
            "dimensions": f"{width}x{height}"
        }

    def extract_audio(self, video_path: str) -> str:
        """Isolated audio extraction for lazy Phase 3 processing."""
        try:
            temp_dir = tempfile.gettempdir()
            audio_path = os.path.join(temp_dir, f"{os.path.basename(video_path)}_audio.wav")
            if os.path.exists(audio_path): return audio_path
            
            print(f"[VideoSampler] [LAZY] Extracting audio: {video_path}")
            subprocess.run([
                "ffmpeg", "-i", video_path, 
                "-vn", "-acodec", "pcm_s16le", "-ar", "16000", "-ac", "1", 
                audio_path, "-y", "-loglevel", "quiet"
            ], check=True)
            return audio_path
        except Exception as e:
            print(f"[VideoSampler] Audio Extraction Failed: {e}")
            return None

    def extract_frames(self, video_path: str, count: int = 8, 특정_indices: list = None):
        """
        V11.1 CPU Optimized: Single-Pass FFmpeg Batch Extraction.
        Extracts all frames in one command, drastically reducing process overhead.
        """
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened(): return [], []
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        cap.release()

        if 특정_indices:
            indices = 특정_indices
        else:
            if total_frames <= count:
                indices = list(range(total_frames))
            else:
                indices = np.linspace(0, total_frames - 1, count, dtype=int)
        
        frames_np = []
        frames_pil = []
        
        # Create a select filter string for the indices
        # Example: select='eq(n\,0)+eq(n\,10)+eq(n\,20)'
        select_filter = "+".join([f"eq(n\,{idx})" for idx in indices])
        
        with tempfile.TemporaryDirectory() as tmpdir:
            out_pattern = os.path.join(tmpdir, "frame_%03d.jpg")
            
            try:
                # Single pass extraction
                cmd = [
                    "ffmpeg", "-i", video_path,
                    "-vf", f"select='{select_filter}'",
                    "-vsync", "0", # vsync 0 is more reliable for select filter
                    "-q:v", "2",
                    out_pattern, "-y", "-loglevel", "quiet"
                ]
                subprocess.run(cmd, check=True)
                
                # Read back the files
                # FFmpeg with vsync 0/vfr might name files frame_001, frame_002...
                # We sort them to ensure chronological order matching our indices
                saved_files = sorted([f for f in os.listdir(tmpdir) if f.startswith("frame_")])
                for f_name in saved_files:
                    out_path = os.path.join(tmpdir, f_name)
                    img = Image.open(out_path).convert("RGB")
                    frames_pil.append(img)
                    frames_np.append(np.array(img))
            except Exception as e:
                print(f"[VideoSampler] Batch FFmpeg failed: {e}. Falling back to iterative extraction.")
                # Fallback: Extract frames one by one if batch fails
                for idx in indices:
                    timestamp = idx / 30.0 # Heuristic if FPS unknown, or use cap.get
                    out_path = os.path.join(tmpdir, f"fb_{idx}.jpg")
                    subprocess.run([
                        "ffmpeg", "-ss", str(max(0, timestamp - 0.1)), "-i", video_path,
                        "-frames:v", "1", out_path, "-y", "-loglevel", "quiet"
                    ])
                    if os.path.exists(out_path):
                        img = Image.open(out_path).convert("RGB")
                        frames_pil.append(img)
                        frames_np.append(np.array(img))

        return frames_np, frames_pil

    def extract_8_frames(self, video_path: str):
        """
        Legacy Method for V10 Pipeline.
        Refactored to NOT extract audio here (Lazy audio is handled by the pipeline).
        """
        info = self.get_info(video_path)
        frames_np, frames_pil = self.extract_frames(video_path, count=8)
        
        return frames_np, frames_pil, {**info, "audio_path": None} 
