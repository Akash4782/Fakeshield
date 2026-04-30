# test_audio_lab_v1.py
import numpy as np
import soundfile as sf
import io
from app.models.audio.audio_detector import analyze_audio

def test_pipeline():
    print("🚀 Starting Audio Lab v1.0 Integration Test")
    
    # Generate 4 seconds of white noise (will pass energy-based VAD)
    sr = 16000
    duration = 4.0
    noise = np.random.normal(0, 0.1, int(sr * duration)).astype(np.float32)
    
    # Save to bytes as WAV
    buf = io.BytesIO()
    sf.write(buf, noise, sr, format='WAV')
    audio_bytes = buf.getvalue()
    
    try:
        print("--- Running Analysis ---")
        result = analyze_audio(audio_bytes, "test_noise.wav")
        
        print("\n✅ Analysis Complete")
        print(f"Verdict:        {result.get('verdict')}")
        print(f"AI Probability: {result.get('ai_probability')}%")
        print(f"Stability:      {result.get('stability_score')}")
        print(f"Fusion Rule:    {result.get('fusion_rule')}")
        
        print("\n--- Signals ---")
        for k, v in result.get('signal_scores', {}).items():
            print(f"  {k:10}: {v}%")
            
        print("\n--- Forensic Summary ---")
        print(result.get('forensic_summary'))
        
        print("\n--- Stability Report ---")
        print(result.get('stability_report'))
        
    except Exception as e:
        print(f"\n❌ Pipeline Failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_pipeline()
