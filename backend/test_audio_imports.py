import torch
print(f"Torch version: {torch.__version__}")
import transformers
print(f"Transformers version: {transformers.__version__}")
import librosa
print("Librosa imported")
import soundfile
print("Soundfile imported")
from app.models.audio.audio_detector import analyze_audio
print("Audio detector imported")
