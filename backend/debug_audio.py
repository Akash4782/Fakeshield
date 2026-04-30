# debug_audio.py
import librosa
import soundfile as sf
import os

path = "dataset/audio/human/female_clear.wav"
print(f"Checking {path}...")

if os.path.exists(path):
    print(f"  Size: {os.path.getsize(path)} bytes")
    try:
        y, sr = sf.read(path)
        print(f"  Soundfile loaded: {sr}Hz, {len(y)} samples")
    except Exception as e:
        print(f"  Soundfile failed: {e}")
        try:
            y, sr = librosa.load(path, sr=None)
            print(f"  Librosa loaded: {sr}Hz, {len(y)} samples")
        except Exception as e2:
            print(f"  Librosa failed: {e2}")
else:
    print("  File not found")
