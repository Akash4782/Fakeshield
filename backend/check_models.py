import os
import sys

def check_all_models():
    print("Checking Text Models...")
    try:
        from app.models.new_forensic_engine import load_models
        load_models()
        print("[SUCCESS] Text Models Loaded Successfully.")
    except Exception as e:
        print(f"[ERROR] Text Models Failed: {e}")

    print("\nChecking Image Models...")
    try:
        from app.models.image_detector import load_image_models
        load_image_models()
        print("[SUCCESS] Image Models Loaded Successfully.")
    except Exception as e:
        print(f"[ERROR] Image Models Failed: {e}")

    print("\nChecking Audio Models...")
    try:
        from app.models.audio.signal_wavlm import _load_model
        _load_model()
        print("[SUCCESS] Audio Models Loaded Successfully.")
    except Exception as e:
        print(f"[ERROR] Audio Models Failed: {e}")

    print("\nChecking Video Models...")
    try:
        from app.models.video_forensics_v2 import load_video_models
        load_video_models()
        print("[SUCCESS] Video Models Loaded Successfully.")
    except Exception as e:
        print(f"[ERROR] Video Models Failed: {e}")

if __name__ == "__main__":
    check_all_models()
