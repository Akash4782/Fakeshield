import os
import sys
import numpy as np
import cv2
from PIL import Image, ImageDraw
import io
import base64

# Add backend to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.models.image_detector import sig_gemini_watermark, create_star_mask

def create_test_image(watermark_size=32, opacity=128, background_type='busy', offset=(10, 10), shape='star'):
    # 1. Create background
    w, h = 800, 600
    if background_type == 'solid':
        img_np = np.zeros((h, w, 3), dtype=np.uint8) + 120
    elif background_type == 'noise':
        img_np = np.random.randint(0, 255, (h, w, 3), dtype=np.uint8)
    else: # busy (gradient + noise)
        img_np = np.zeros((h, w, 3), dtype=np.uint8)
        for i in range(h):
            img_np[i, :, 0] = int(255 * i / h)
            img_np[i, :, 1] = int(255 * (h-i) / h)
        img_np = (img_np * 0.5 + np.random.randint(0, 100, (h, w, 3)) * 0.5).astype(np.uint8)

    img_pil = Image.fromarray(img_np)
    
    # 2. Create watermark/shape
    if shape == 'star':
        mask = create_star_mask(watermark_size)
    else: # square
        mask = np.zeros((watermark_size, watermark_size), dtype=np.uint8) + 255
        
    star_rgba = np.zeros((watermark_size, watermark_size, 4), dtype=np.uint8)
    star_rgba[:, :, 0:3] = 255 # White
    star_rgba[:, :, 3] = (mask > 0).astype(np.uint8) * opacity
    
    star_pil = Image.fromarray(star_rgba, mode='RGBA')
    
    # 3. Paste watermark in bottom right with offset
    pos = (w - watermark_size - offset[0], h - watermark_size - offset[1])
    img_pil.paste(star_pil, pos, star_pil)
    
    return img_pil

def run_test():
    print("--- Gemini Watermark Detection Test ---")
    
    test_cases = [
        ("Solid, standard", 32, 200, 'solid', (10, 10)),
        ("Noise, faint", 28, 80, 'noise', (15, 15)),
        ("Busy, small", 20, 150, 'busy', (5, 5)),
        ("Busy, large, offset", 64, 180, 'busy', (50, 50)),
        ("Very faint, tiny", 16, 40, 'solid', (10, 10)),
        ("FP: Generic Square", 32, 255, 'solid', (20, 20), True), # Square
        ("FP: Text Block", 24, 255, 'busy', (30, 30), True), # Solid block
    ]
    
    for case in test_cases:
        if len(case) == 6:
            name, size, opacity, bg, offset, is_fp = case
        else:
            name, size, opacity, bg, offset = case
            is_fp = False
            
        print(f"\nTesting: {name}")
        print(f"  Params: size={size}, opacity={opacity}, bg={bg}, offset={offset}")
        
        if is_fp:
            # Create a square instead of a star
            img = create_test_image(size, opacity, bg, offset, shape='square')
        else:
            img = create_test_image(size, opacity, bg, offset, shape='star')
            
        detected, vis = sig_gemini_watermark(img)
        
        if detected:
            if is_fp:
                print(f"  [CRITICAL FAILURE] False Positive detected on a generic shape!")
            else:
                print(f"  [SUCCESS] Detected! Visualization length: {len(vis) if vis else 0}")
        else:
            if is_fp:
                print(f"  [SUCCESS] Correctly ignored generic shape.")
            else:
                print(f"  [FAILURE] Watermark not detected.")

if __name__ == "__main__":
    run_test()
