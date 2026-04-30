import cv2
import numpy as np

def create_star_mask(size):
    mask = np.zeros((size, size), dtype=np.uint8)
    center = size / 2.0
    for y in range(size):
        for x in range(size):
            nx = (x - center + 0.5) / center
            ny = (y - center + 0.5) / center
            if (abs(nx)**0.65 + abs(ny)**0.65) <= 1.0:
                mask[y, x] = 255
    return mask

def get_star_edge_template(size):
    mask = create_star_mask(size)
    edges = cv2.Canny(mask, 100, 200)
    return edges

def test():
    # Create fake image with star
    img = np.ones((200, 200), dtype=np.uint8) * 120
    # Add noise
    noise = np.random.normal(0, 10, img.shape).astype(np.int16)
    img = np.clip(img.astype(np.int16) + noise, 0, 255).astype(np.uint8)
    
    # insert star (size 34) at bottom right
    star_mask = create_star_mask(34)
    # simulate transparent watermark (make it slightly brighter)
    sy, sx = 150, 150
    region = img[sy:sy+34, sx:sx+34].copy().astype(np.float32)
    star_f = star_mask.astype(np.float32) / 255.0
    
    # blend
    blended = region * (1 - star_f) + (region + 60) * star_f
    img[sy:sy+34, sx:sx+34] = np.clip(blended, 0, 255).astype(np.uint8)
    
    # Edge detection
    edges_img = cv2.Canny(img, 50, 150)
    
    # Multi-scale match
    sizes = range(20, 50, 2)
    max_val_global = 0
    best_size = 0
    best_loc = None
    
    for s in sizes:
        tpl = get_star_edge_template(s)
        if tpl.shape[0] > edges_img.shape[0] or tpl.shape[1] > edges_img.shape[1]:
            continue
        res = cv2.matchTemplate(edges_img, tpl, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        if max_val > max_val_global:
            max_val_global = max_val
            best_size = s
            best_loc = max_loc
            
    print(f"Max match: {max_val_global:.4f} at size {best_size}, loc {best_loc}")

if __name__ == '__main__':
    test()
