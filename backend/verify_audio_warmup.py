
import sys
import os

# Add backend to path
sys.path.append(os.path.abspath("."))

from app.models.audio.audio_warmup import warm_up_audio_models

if __name__ == "__main__":
    print("Testing Audio Model Warmup...")
    try:
        warm_up_audio_models()
        print("\nSUCCESS: All models loaded sequentially without meta tensor errors.")
    except Exception as e:
        print(f"\nFAILURE: {e}")
        sys.exit(1)
