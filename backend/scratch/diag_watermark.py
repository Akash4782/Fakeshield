import cv2
import numpy as np
from PIL import Image
import io
import base64

def create_star_mask(size: int) -> np.ndarray:
    mask = np.zeros((size, size), dtype=np.uint8)
    center = size / 2.0
    for y in range(size):
        for x in range(size):
            nx = (x - center + 0.5) / center
            ny = (y - center + 0.5) / center
            if (abs(nx)**0.65 + abs(ny)**0.65) <= 1.0:
                mask[y, x] = 255
    return mask

def verify_gemini_geometry(roi: np.ndarray, size: int) -> float:
    try:
        h, w = roi.shape[:2]
        if h < size or w < size:
            return 0.0
        
        # 1. Saturation Veto
        if len(roi.shape) == 3:
            hsv = cv2.cvtColor(roi, cv2.COLOR_RGB2HSV)
            avg_sat = hsv[:, :, 1].mean()
            print(f"DEBUG: avg_sat = {avg_sat}")
            if avg_sat > 50:
                print("DEBUG: Saturation Veto triggered!")
                return 0.0
        
        gray = cv2.cvtColor(roi, cv2.COLOR_RGB2GRAY) if len(roi.shape) == 3 else roi
        roi_std = cv2.resize(gray, (size, size))
        
        k_size = max(3, size // 3)
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (k_size, k_size))
        tophat = cv2.morphologyEx(roi_std, cv2.MORPH_TOPHAT, kernel)
        
        _, thresh = cv2.threshold(tophat, 40, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        h_flip = cv2.flip(roi_std, 1)
        v_flip = cv2.flip(roi_std, 0)
        sim_h = cv2.matchTemplate(roi_std, h_flip, cv2.TM_CCOEFF_NORMED)[0, 0]
        sim_v = cv2.matchTemplate(roi_std, v_flip, cv2.TM_CCOEFF_NORMED)[0, 0]
        sym_score = (max(0, sim_h) + max(0, sim_v)) / 2.0
        
        fullness = np.count_nonzero(thresh) / (size * size)
        if 0.20 < fullness < 0.45:
            conc_score = 1.0
        else:
            conc_score = max(0, 1.0 - abs(fullness - 0.33) * 6.0)
            
        m = size // 2
        t1, t2, t3, t4 = int(thresh[0, m]), int(thresh[size-1, m]), int(thresh[m, 0]), int(thresh[m, size-1])
        print(f"DEBUG: points = {t1}, {t2}, {t3}, {t4}")
        if (t1 + t2 + t3 + t4) / 4.0 < 120:
            print("DEBUG: Point Veto triggered!")
            return 0.0
            
        q = max(2, size // 8)
        corners = thresh[:q, :q].mean() + thresh[:q, -q:].mean() + thresh[-q:, :q].mean() + thresh[-q:, -q:].mean()
        print(f"DEBUG: corners = {corners}")
        if corners > 30:
            print("DEBUG: Corner Veto triggered!")
            return 0.0
            
        return (sym_score * 0.3) + (conc_score * 0.3) + 0.4
    except Exception as e:
        print(f"DEBUG: Error in verify: {e}")
        return 0.0

# Mock an image with a watermark on a brown background
# Brown: (139, 69, 19) in RGB.
# Let's see its saturation.
brown = np.array([[[139, 69, 19]]], dtype=np.uint8)
hsv_brown = cv2.cvtColor(brown, cv2.COLOR_RGB2HSV)
print(f"Brown saturation: {hsv_brown[0,0,1]}") # Output should be around 220

# Create a region that is brown with a white star
size = 32
roi = np.full((size, size, 3), [139, 69, 19], dtype=np.uint8)
mask = create_star_mask(size)
# Blend white star (semi-transparent)
roi[mask > 0] = (roi[mask > 0] * 0.5 + np.array([255, 255, 255]) * 0.5).astype(np.uint8)

print("Running verification on mock brown ROI...")
score = verify_gemini_geometry(roi, size)
print(f"Final Geometric Score: {score}")
