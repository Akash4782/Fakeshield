import cv2, os, numpy as np

def get_stats(p): 
    img = cv2.imread(p, 0)
    if img is None: return 0.0, 0.0
    c = cv2.resize(img, (256, 256))
    f = np.fft.fft2(c); fs = np.fft.fftshift(f); mag = 20*np.log(np.abs(fs)+1e-9)
    m = np.zeros((256, 256)); cv2.circle(m, (128,128), 110, 1, -1); im = 1 - m
    outer = np.mean(mag[im>0])
    
    bl = cv2.medianBlur(img, 5); res = cv2.absdiff(img, bl)
    hist = cv2.calcHist([res], [0], None, [256], [0, 256])
    hist /= hist.sum(); ent = -np.sum(hist * np.log2(hist + 1e-7))
    return outer, ent

import os
for f in os.listdir('evaluation_dataset/real'):
    p = os.path.join('evaluation_dataset/real', f)
    o, e = get_stats(p)
    print(f'REAL {f}: Eng={o:.2f}, Ent={e:.2f}')

for f in os.listdir('evaluation_dataset/ai'):
    p = os.path.join('evaluation_dataset/ai', f)
    o, e = get_stats(p)
    print(f'AI {f}: Eng={o:.2f}, Ent={e:.2f}')
