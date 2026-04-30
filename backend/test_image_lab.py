import asyncio
import base64
import io
from PIL import Image
from app.services.image_pipeline import run_image_pipeline

async def test_pipeline():
    # 1. Create a dummy solid color image (Real-looking noise-free)
    img = Image.new('RGB', (512, 512), color=(73, 109, 137))
    buf = io.BytesIO()
    img.save(buf, format='JPEG')
    image_bytes = buf.getvalue()

    print("--- Running AI Image Forensic Pipeline v8.1 ---")
    try:
        result = await run_image_pipeline(image_bytes)
        
        print(f"Verdict: {result['verdict']} ({result['threat_level']})")
        print(f"AI Probability: {result['ai_probability']}")
        print(f"Confidence: {result['confidence']}%")
        print("\nSignals:")
        for k, v in result['signals'].items():
            print(f"  - {k}: {v}")
        
        print("\nReasons:")
        for r in result['reasons']:
            print(f"  - {r}")
            
        print(f"\nProcessing Time: {result['processing_time']}s")
        print("-----------------------------------------------")
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"Test Failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_pipeline())
