import cv2
import numpy as np
from PIL import Image, ImageChops, ImageDraw
import io

def detect_tampered_watermark_ela(img_pil: Image.Image) -> tuple[float, bool]:
    # 1. ELA
    buf = io.BytesIO()
    img_pil.save(buf, 'JPEG', quality=95)
    recompressed = Image.open(buf)
    ela = ImageChops.difference(img_pil, recompressed)
    ela_gray = np.array(ela.convert('L'), dtype=np.float32)
    
    # 2. ROI
    w, h = img_pil.size
    crop_w = min(250, int(w * 0.20))
    crop_h = min(250, int(h * 0.20))
    if crop_w < 50 or crop_h < 50:
         return 0.0, False
         
    roi_ela = ela_gray[-crop_h:, -crop_w:]
    rest_ela = ela_gray[:-crop_h, :-crop_w]
    
    mean_rest = np.mean(rest_ela)
    mean_roi = np.mean(roi_ela)
    std_roi = np.std(roi_ela)
    
    # Inpainted regions often have strongly divergent ELA blocks.
    # Look for a localized spike in ELA variance or max ELA in the ROI.
    # Or simply compare max error.
    
    # Calculate localized ELA max via windowing to find hot spots
    kernel = np.ones((15, 15), dtype=np.float32) / 225.0
    local_ela_mean = cv2.filter2D(roi_ela, -1, kernel)
    
    max_local_ela = np.max(local_ela_mean)
    
    # Anomaly flag if there's a highly anomalous ELA patch
    anomaly_ratio = max_local_ela / (mean_rest + 1e-6)
    
    print(f"Mean Rest: {mean_rest:.2f}, Max Local ROI: {max_local_ela:.2f}, Ratio: {anomaly_ratio:.2f}")
    
    is_tampered = anomaly_ratio > 3.0 # threshold
    return float(anomaly_ratio), bool(is_tampered)

def test():
    # Simulate an image
    img = Image.new('RGB', (800, 800), color=(15, 15, 20))
    # add some texture
    arr = np.array(img).astype(np.float32)
    arr += np.random.normal(0, 5, arr.shape)
    img = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))
    
    # Save it to establish baseline compression
    buf = io.BytesIO()
    img.save(buf, 'JPEG', quality=80)
    baseline_img = Image.open(buf).convert('RGB')
    
    score, is_tampered = detect_tampered_watermark_ela(baseline_img)
    print("Baseline (Authentic):", score, is_tampered)
    
    # Now tamper it: heal the bottom right corner
    tampered_arr = np.array(baseline_img)
    tampered_arr[-100:-50, -100:-50] = [15, 15, 20] # healed black patch
    
    tampered_img = Image.fromarray(tampered_arr)
    # the user then saves the tampered image (Photoshop export)
    buf2 = io.BytesIO()
    tampered_img.save(buf2, 'JPEG', quality=90)
    healed_img = Image.open(buf2).convert('RGB')
    
    score2, is_tampered2 = detect_tampered_watermark_ela(healed_img)
    print("Tampered (Healed):", score2, is_tampered2)

if __name__ == "__main__":
    test()
