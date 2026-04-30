import torch
import numpy as np
import time
import os
import sys

# Add current dir to sys.path
sys.path.append(os.getcwd())

from app.models.audio.audio_detector import analyze_audio

def verify():
    print("Starting optimization verification...")
    
    # Generate 10 seconds of "audio" (Gaussian noise)
    sr = 16000
    duration = 10
    waveform = np.random.normal(0, 0.1, sr * duration).astype(np.float32)
    
    # Mock audio bytes (this is tricky because load_audio uses soundfile/librosa on bytes)
    # Let's just mock the 'Audio' object if we want to test detector internals,
    # but it's better to test the whole path.
    
    # We'll use a real sine wave saved to a temp file then read as bytes
    import soundfile as sf
    import io
    
    buf = io.BytesIO()
    sf.write(buf, waveform, sr, format='WAV')
    audio_bytes = buf.getvalue()
    
    print(f"Test audio generated: {len(audio_bytes)} bytes")
    
    start_time = time.time()
    try:
        result = analyze_audio(audio_bytes, "test_audio.wav")
        elapsed = time.time() - start_time
        
        print(f"\n✅ Analysis Finished in {elapsed:.2f} seconds")
        print(f"Result Verdict: {result.get('verdict', 'N/A')}")
        print(f"AI Probability: {result.get('ai_probability', 'N/A')}")
        print(f"Signals Agreement: {result.get('agreement', 'N/A')}")
        print("\nSignal Scores:")
        for name, score in result.get('signal_scores', {}).items():
            print(f"  - {name}: {score}%")
            
        # Check for WavLM success
        wavlm_score = result.get('signal_scores', {}).get('wavlm', 50.0)
        if wavlm_score != 50.0:
            print("✅ WavLM successfully returned a non-base score (Device meta fix confirmed).")
        else:
            print("⚠️ WavLM returned exactly 50.0. This might be legitimate for noise, but verify it didn't fail.")
            
        print("\nSignal Details (check for errors):")
        for name, detail in result.get('signal_details', {}).items():
            if 'error' in detail or 'reason' in detail:
                 print(f"  - {name}: {detail}")
            
    except Exception as e:
        import traceback
        print(f"❌ Analysis failed: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    verify()
