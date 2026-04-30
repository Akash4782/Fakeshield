import cv2
import numpy as np
from PIL import Image
import os
import sys

# Add backend to path to import detector
sys.path.append(os.path.abspath("backend"))
from app.models.image_detector import sig_gemini_watermark

def test_blank_images():
    print("Testing blank and noisy images for Gemini watermark false positives...")
    
    # 1. Pure white image
    white_img = Image.fromarray(np.full((1024, 1024, 3), 255, dtype=np.uint8))
    found, _ = sig_gemini_watermark(white_img)
    print(f"White image: {'FAILED (Found)' if found else 'PASSED (Not found)'}")
    
    # 2. Random noise (low intensity)
    noise_img = Image.fromarray(np.random.randint(200, 255, (1024, 1024, 3), dtype=np.uint8))
    found, _ = sig_gemini_watermark(noise_img)
    print(f"Low-intensity noise: {'FAILED (Found)' if found else 'PASSED (Not found)'}")

    # 3. Fabric-like texture (light gray with some lines)
    fabric = np.full((1024, 1024, 3), 230, dtype=np.uint8)
    for i in range(0, 1024, 20):
        cv2.line(fabric, (i, 0), (i+100, 1024), (220, 220, 220), 2)
    fabric_img = Image.fromarray(fabric)
    found, _ = sig_gemini_watermark(fabric_img)
    print(f"Fabric texture: {'FAILED (Found)' if found else 'PASSED (Not found)'}")

if __name__ == "__main__":
    test_blank_images()
