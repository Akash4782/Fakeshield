import cv2
import numpy as np
from app.models.image_detector_v20 import FakeShieldV20

path1 = 'evaluation_dataset/real/portrait.jpg'
path2 = 'evaluation_dataset/ai/portrait_ai.png'

print("PORTRAIT TESTS")
engine = FakeShieldV20()
res_real = engine.analyze(path1)
print("REAL PORTRAIT:", res_real["signals"])
res_ai = engine.analyze(path2)
print("AI PORTRAIT:", res_ai["signals"])
