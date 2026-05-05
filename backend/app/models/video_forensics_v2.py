import numpy as np
import cv2
from scipy import ndimage

class VideoForensicsV2:
    """Detects PRNU cross-frame inconsistencies and spectral decay offsets (FFT)"""
    
    def extract_noise_residual(self, img_bgr):
        """Extracts sensor noise residual by Gaussian de-noising (Optimized)"""
        # CPU Optimization: Downsample if image is too large for fast Gaussian filtering
        h, w = img_bgr.shape[:2]
        max_dim = 720
        if max(h, w) > max_dim:
            scale = max_dim / max(h, w)
            img_bgr = cv2.resize(img_bgr, (int(w * scale), int(h * scale)))
            
        gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY).astype(np.float64)
        # Denoiser acts as a high-pass filter
        denoised = ndimage.gaussian_filter(gray, sigma=2.0)
        noise = gray - denoised
        return noise

    def analyze_prnu_consistency(self, frames_bgr: list) -> dict:
        """Measures cross-frame correlation of sensor noise patterns"""
        if len(frames_bgr) < 2: return {"score": 0.5, "corr": 0.0}
        
        # Parallelize noise extraction if needed, but for 8 frames, sequential is fine on CPU
        residuals = [self.extract_noise_residual(f) for f in frames_bgr]
        correlations = []
        
        for i in range(len(residuals) - 1):
            r1 = residuals[i].flatten()
            r2 = residuals[i+1].flatten()
            
            # Cross-correlation between frame noise residuals
            corr = np.corrcoef(r1, r2)[0,1]
            if not np.isnan(corr):
                correlations.append(corr)
                
        if not correlations: return {"score": 0.5, "corr": 0.0}
        
        mean_corr = np.mean(correlations)
        # Real Camera: Consistent noise patterns across frames (same sensor) -> High correlation
        # AI Video: Synthetic noise patterns (per-frame generation) -> Low correlation
        
        prnu_ai = max(min(1.0 - (mean_corr - 0.01) / 0.1, 1.0), 0.01)
        
        return {
            "score": float(prnu_ai),
            "correlation": float(mean_corr),
            "noise_std": float(np.std([np.std(r) for r in residuals]))
        }

    def analyze_fft_spectrum(self, img_bgr) -> float:
        """Analyzes spectral decay curve (1/f² law) for GAN/Diffusion artifacts (Optimized)"""
        # CPU Optimization: FFT is O(N log N), but N = H*W. Reducing H,W helps.
        h, w = img_bgr.shape[:2]
        if max(h, w) > 512:
            scale = 512 / max(h, w)
            img_bgr = cv2.resize(img_bgr, (int(w * scale), int(h * scale)))

        gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY).astype(np.float64)
        
        # 2D Fast Fourier Transform
        f = np.fft.fft2(gray)
        f_shift = np.fft.fftshift(f)
        magnitude_spectrum = 20 * np.log(np.abs(f_shift) + 1e-9)
        
        # Calculate radially averaged power spectrum
        h, w = gray.shape
        cy, cx = h//2, w//2
        y, x = np.ogrid[:h, :w]
        r = np.sqrt((x - cx)**2 + (y - cy)**2).astype(np.int64)
        
        tbin = np.bincount(r.ravel(), magnitude_spectrum.ravel())
        nr = np.bincount(r.ravel())
        radial_profile = tbin / nr
        
        # AI-generated content often has artifacts in the high frequencies
        high_freq_signal = np.mean(radial_profile[int(len(radial_profile)*0.7):])
        
        fft_ai = min(max((high_freq_signal / 50.0), 0.0), 1.0)
        return float(fft_ai)

    def get_signal(self, frames_bgr: list) -> dict:
        """Ensembles PRNU and FFT signals"""
        if not frames_bgr: return {"score": 0.5, "fft_score": 0.5, "prnu_score": 0.5}
        
        prnu = self.analyze_prnu_consistency(frames_bgr)
        fft_scores = [self.analyze_fft_spectrum(f) for f in frames_bgr]
        fft_mean = np.mean(fft_scores)
        
        ensemble_score = (prnu["score"] * 0.6 + fft_mean * 0.4)
        
        return {
            "score": float(ensemble_score),
            "prnu_score": prnu["score"],
            "fft_score": float(fft_mean),
            "prnu_correlation": prnu["correlation"]
        }
