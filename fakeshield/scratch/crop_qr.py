from PIL import Image
import os

img_path = r'C:\Users\office\.gemini\antigravity\brain\84268cb7-b661-4045-ae4c-a56ae6646f85\media__1777712422485.png'
save_path = r'c:\Users\office\Documents\Final_year_project\fakeshield\src\assets\payment-qr.png'

img = Image.open(img_path)
# Crop coordinates: (left, top, right, bottom)
# Estimating based on 737x1024
# The white box is roughly from (100, 210) to (637, 810)
# The QR code itself is inside that.
qr_crop = img.crop((130, 230, 610, 710))
qr_crop.save(save_path)
print(f"Saved cropped QR to {save_path}")
