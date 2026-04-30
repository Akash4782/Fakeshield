import cv2
import numpy as np
import scipy.ndimage as ndimage

def calculate_noise_residual(image: np.ndarray) -> np.ndarray:
    """Extract noise using median filter subtraction."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY).astype(np.float32)
    blur = ndimage.median_filter(gray, size=3)
    return gray - blur

def detect_inpainting_anomaly(image: np.ndarray) -> tuple[float, bool]:
    """
    Looks for localized loss of camera noise in the bottom right quadrant.
    """
    h, w = image.shape[:2]
    # Crop bottom right 300x300, or 25% of image
    crop_w = min(300, int(w * 0.25))
    crop_h = min(300, int(h * 0.25))
    
    if crop_w < 50 or crop_h < 50:
        return 0.0, False
        
    roi = image[h-crop_h:, w-crop_w:]
    noise = calculate_noise_residual(roi)
    
    # Calculate local variance using window
    window_size = 20
    # Create variance map
    sq_noise = noise ** 2
    kernel = np.ones((window_size, window_size)) / (window_size * window_size)
    local_variance = cv2.filter2D(sq_noise, -1, kernel)
    
    # We are looking for regions where variance is anomalously low (inpainting is smooth)
    # compared to the surrounding region.
    # Exclude absolute margins to avoid edge artifacts
    local_variance = local_variance[window_size:-window_size, window_size:-window_size]
    
    if local_variance.size == 0:
         return 0.0, False
    
    mean_var = np.mean(local_variance)
    min_var = np.min(local_variance)
    
    if mean_var < 1.0:
        # The entire region is already flat (e.g., clear sky, solid background)
        # We can't definitively say it was inpainted if the whole thing is smooth
        return 0.0, False
        
    # Anomaly Ratio
    anomaly_ratio = min_var / (mean_var + 1e-6)
    
    # If the minimum variance is less than 5% of the average variance of the region
    # it implies a completely smooth synthetic patch in an otherwise noisy area.
    # We return an anomaly score (higher is more anomalous).
    anomaly_score = max(0.0, 1.0 - (anomaly_ratio * 10))
    is_tampered = anomaly_score > 0.8  # meaning min_var is < 2% of mean_var
    
    return float(anomaly_score), bool(is_tampered)

def test():
    # 1. Create a "real" noisy image
    base = np.ones((400, 400, 3), dtype=np.uint8) * 128
    noise = np.random.normal(0, 15, base.shape)
    img = np.clip(base + noise, 0, 255).astype(np.uint8)
    
    # 2. Add an "inpainted" region at bottom right (where watermark used to be)
    # user heals a 60x60 patch, removing all noise
    img[320:380, 400-80:400-20] = 125 # smooth color, no noise
    
    score, is_tampered = detect_inpainting_anomaly(img)
    print(f"[Anomalous Healed] Score: {score:.3f}, Tampered? {is_tampered}")
    
    # 3. Test on completely clean image (flat color, no noise)
    flat_img = np.ones((400, 400, 3), dtype=np.uint8) * 128
    score2, is_tampered2 = detect_inpainting_anomaly(flat_img)
    print(f"[Flat Sky / No Noise] Score: {score2:.3f}, Tampered? {is_tampered2}")
    
    # 4. Test on uniform noise
    noisy_img = np.clip(base + np.random.normal(0, 15, base.shape), 0, 255).astype(np.uint8)
    score3, is_tampered3 = detect_inpainting_anomaly(noisy_img)
    print(f"[Uniformly Noisy Photo] Score: {score3:.3f}, Tampered? {is_tampered3}")

if __name__ == "__main__":
    test()
