import asyncio
import base64
import io
import time
from PIL import Image
from app.models.image_detector import analyze_image

async def test_pipeline():
    # 1. Create a dummy solid color image (Real-looking noise-free)
    img = Image.new('RGB', (512, 512), color=(73, 109, 137))
    buf = io.BytesIO()
    img.save(buf, format='JPEG')
    image_bytes = buf.getvalue()

    print("--- Running AI Image Forensic Pipeline v8.0 (Batched) ---")
    t0 = time.time()
    try:
        # analyze_image is synchronous, but we can run it in a thread for realism
        result = await asyncio.to_thread(analyze_image, image_bytes)
        elapsed = time.time() - t0
        
        print(f"Verdict: {result['verdict']} ({result['threat_level']})")
        print(f"AI Probability: {result['ai_probability']}")
        print(f"Confidence: {result['confidence']}%")
        print(f"Processing Time: {result['processing_time']}")
        print(f"Wall Clock Time: {elapsed:.2f}s")
        
        print("\nSignals:")
        for k, v in result['signals'].items():
            print(f"  - {k}: {v}")
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"Test Failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_pipeline())
