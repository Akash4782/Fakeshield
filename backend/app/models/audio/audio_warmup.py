from .signal_wavlm import _load_model as load_wavlm
from .signal_wav2vec import _load_model as load_wav2vec


def warm_up_audio_models():
    """
    Warms up audio deepfake detection models at startup.
    This prevents race conditions during parallel inference dispatch.
    """
    print("  [STEP 2/4] Pre-loading Audio Forensic Models...")
    
    # Load sequentially to avoid meta-tensor issues
    try:
        print("      [1/2] Loading WavLM signal...")
        load_wavlm()
        print("         [OK] WavLM signal ready.")
    except Exception as e:
        print(f"         [FAIL] WavLM pre-load failed: {e}")

    try:
        print("      [2/2] Loading AST/Wav2Vec signal...")
        load_wav2vec()
        print("         [OK] AST/Wav2Vec signal ready.")
    except Exception as e:
        print(f"         [FAIL] AST/Wav2Vec pre-load failed: {e}")

    print("  [OK] Audio models pre-loaded.")
