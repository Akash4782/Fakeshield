import torch
import torchvision.models.optical_flow as of_models
import torchvision.transforms.functional as F_tv
import numpy as np
import cv2
import base64
import io
from PIL import Image
from app.models.loader_sync import MODEL_LOAD_LOCK

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

class VideoTempoRaft:
    """Uses RAFT (Recurrent All-Pairs Field Transforms) for dense motion consistency"""
    
    def __init__(self):
        print(f"[VideoTempoRaft] Loading RAFT on {DEVICE}...")
        with MODEL_LOAD_LOCK:
            self.model = of_models.raft_small(pretrained=True).to(DEVICE).eval()

    def preprocess(self, img_bgr):
        """Converts BGR to RGB and resizes to multiple of 8"""
        img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
        h, w = img_rgb.shape[:2]
        
        # Compact resolution constraint (256 max dimension) for speed
        max_dim = 256
        if max(h, w) > max_dim:
            scale = max_dim / max(h, w)
            img_rgb = cv2.resize(img_rgb, (int(w * scale), int(h * scale)))
            h, w = img_rgb.shape[:2]
            
        # Guarantee minimum dimension of 128 for RAFT downsampling compatibility
        if min(h, w) < 128:
            scale = 128 / min(h, w)
            img_rgb = cv2.resize(img_rgb, (int(w * scale), int(h * scale)))
            h, w = img_rgb.shape[:2]

        h8 = (h // 8) * 8
        w8 = (w // 8) * 8
        img_rgb = cv2.resize(img_rgb, (w8, h8))
        
        img_t = torch.from_numpy(img_rgb).permute(2, 0, 1).float() / 255.0
        return img_t.unsqueeze(0).to(DEVICE)

    @torch.no_grad()
    def compute_flow(self, img1, img2):
        """Calculates optical flow between two frames"""
        t1 = self.preprocess(img1)
        t2 = self.preprocess(img2)
        
        predictions = self.model(t1, t2)
        flow = predictions[-1].squeeze(0).permute(1, 2, 0).cpu().numpy()
        return flow

    def flow_to_image(self, flow):
        """Converts optical flow into an RGB heatmap for visualization"""
        h, w = flow.shape[:2]
        hsv = np.zeros((h, w, 3), dtype=np.uint8)
        hsv[..., 1] = 255
        
        mag, ang = cv2.cartToPolar(flow[..., 0], flow[..., 1])
        hsv[..., 0] = ang * 180 / np.pi / 2
        hsv[..., 2] = cv2.normalize(mag, None, 0, 255, cv2.NORM_MINMAX)
        
        bgr = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        return bgr

    def get_signal(self, frames_bgr: list) -> dict:
        """Analyzes motion consistency across a sequence of frames"""
        if len(frames_bgr) < 2: return {"score": 0.5, "conf": 0.0}
        
        # CPU OPTIMIZATION: Pre-process all frames in one batch
        # This avoids redundant color conversion and resizing for shared frames in pairs
        preprocessed_tensors = [self.preprocess(f) for f in frames_bgr]
        
        flows = []
        magnitudes = []
        
        # Batch inference loop
        for i in range(len(preprocessed_tensors) - 1):
            t1 = preprocessed_tensors[i]
            t2 = preprocessed_tensors[i+1]
            
            with torch.no_grad():
                predictions = self.model(t1, t2)
                flow = predictions[-1].squeeze(0).permute(1, 2, 0).cpu().numpy()
            
            flows.append(flow)
            mag = np.sqrt(flow[..., 0]**2 + flow[..., 1]**2)
            magnitudes.append(mag)
            
        # 1. Variance of Magnitude (Motion Jitter)
        mag_vars = [np.var(m) for m in magnitudes]
        mag_means = [np.mean(m) for m in magnitudes]
        
        # PAVR (Peak-to-Average Velocity Ratio) - Detects sudden 'morphing' spikes
        peak = np.max(mag_means)
        avg = np.mean(mag_means)
        pavr = peak / (avg + 1e-9)
        
        # 2. Flow Entropy (Spatial Randomness)
        flow_entropy = np.mean([float(-np.sum((m/(m.sum()+1e-8))*np.log(m/(m.sum()+1e-8)+1e-8))) for m in magnitudes])
        
        # 3. Temporal Coherence (Residuals)
        # Difference between consecutive flow maps (should be small in real video)
        residuals = []
        for i in range(len(flows) - 1):
            res = np.mean(np.abs(flows[i+1] - flows[i]))
            residuals.append(float(res))
        
        avg_residual = np.mean(residuals) if residuals else 0.0
        
        # Evidence Extraction: Find the frame with highest PAVR
        max_idx = np.argmax(mag_means)
        evidence_bgr = self.flow_to_image(flows[max_idx])
        
        # Convert to Base64 for frontend display
        _, buffer = cv2.imencode('.jpg', evidence_bgr)
        evidence_b64 = base64.b64encode(buffer).decode('utf-8')
        
        # Score Logic (Consistency Auditor v11.0 - Refined)
        ai_prob = 0.25 
        if pavr > 5.0: ai_prob += 0.25
        if flow_entropy > 4.5: ai_prob += 0.2
        if avg_residual > 4.0: ai_prob += 0.2
        if np.std(mag_vars) > 3.0: ai_prob += 0.1
        
        ai_prob = min(max(ai_prob, 0.01), 0.99)
        
        return {
            "score": float(ai_prob),
            "pavr": float(pavr),
            "avg_residual": float(avg_residual),
            "flow_entropy": float(flow_entropy),
            "mag_timeline": [float(m) for m in mag_means],
            "evidence_heatmap": f"data:image/jpeg;base64,{evidence_b64}"
        }
