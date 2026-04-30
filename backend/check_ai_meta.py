# check_ai_meta.py
import librosa
import os

AI_DIR = "dataset/audio/ai"
if not os.path.exists(AI_DIR): AI_DIR = "dataset/audio/AI"

for f in os.listdir(AI_DIR):
    path = os.path.join(AI_DIR, f)
    try:
        y, sr = librosa.load(path, sr=None)
        print(f"{f}: {len(y)/sr:.1f}s, {sr}Hz")
    except Exception as e:
        print(f"{f}: Failed to load ({e})")
