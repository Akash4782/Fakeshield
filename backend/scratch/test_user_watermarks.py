
import sys
import os
import io
import base64
import numpy as np
import cv2
from PIL import Image

# Add backend to path
sys.path.append(r'c:\Users\office\Documents\Final_year_project\backend')

from app.models.image_detector import sig_gemini_watermark, verify_gemini_geometry

def test_image(image_path, name):
    print(f"\n--- Testing {name} ---")
    img = Image.open(image_path).convert("RGB")
    
    # Since sig_gemini_watermark looks in the bottom-right 30%, 
    # and the user provided small crops, we need to pad them 
    # or simulate them being in the bottom-right.
    
    w, h = img.size
    # Create a larger canvas (1000x1000) and put the crop in the bottom-right
    canvas = Image.new('RGB', (1000, 1000), (0, 0, 0))
    canvas.paste(img, (1000-w, 1000-h))
    
    detected, vis = sig_gemini_watermark(canvas)
    
    print(f"Detection Result: {detected}")
    if detected:
        # Save visualization to see where it matched
        vis_data = base64.b64decode(vis)
        with open(f"c:\\Users\\office\\Documents\\Final_year_project\\backend\\scratch\\{name}_vis.png", "wb") as f:
            f.write(vis_data)
        print(f"Visualization saved to {name}_vis.png")
    else:
        # If not detected, let's probe deeper
        w_c, h_c = canvas.size
        crop_w = min(350, int(w_c * 0.30))
        crop_h = min(350, int(h_c * 0.30))
        region = canvas.crop((w_c - crop_w, h_c - crop_h, w_c, h_c))
        roi_np = np.array(region)
        
        # Check saturation
        hsv = cv2.cvtColor(roi_np, cv2.COLOR_RGB2HSV)
        avg_sat = hsv[:, :, 1].mean()
        print(f"Average Saturation in ROI: {avg_sat:.2f}")
        
        # Try verify_gemini_geometry directly on the crop
        # We need to find the sparkle in the crop first, but since the crop IS the sparkle area:
        # Let's try multiple sizes
        roi_gray = cv2.cvtColor(roi_np, cv2.COLOR_RGB2GRAY)
        for s in [16, 20, 24, 28, 32, 40, 48]:
            if s > w or s > h: continue
            # Take a center crop of the original user image (which is the sparkle)
            start_y = max(0, (h - s) // 2)
            start_x = max(0, (w - s) // 2)
            sparkle_roi = np.array(img)[start_y:start_y+s, start_x:start_x+s]
            if sparkle_roi.shape[0] == s and sparkle_roi.shape[1] == s:
                geom = verify_gemini_geometry(sparkle_roi, s)
                if geom > 0:
                    print(f"  Geom Match at size {s}: {geom:.3f}")
                else:
                    print(f"  Geom Failed at size {s}")

if __name__ == "__main__":
    # Use the images provided by the user (input_file_0.png and input_file_1.png)
    # I'll need to know their actual paths. Usually they are in the context.
    # I'll assume they are the first two media files.
    # For now, I'll use the placeholder paths if I can find them or just use the tool.
    
    # Wait, I don't have the paths directly. I'll search for them in the workspace.
    # Actually, they might be in a temporary location.
    pass
