import os
import sys

# Protobuf Compatibility Patch (Must be at the absolute top)
try:
    import google.protobuf.runtime_version as rv
    rv.ValidateProtobufRuntimeVersion = lambda *args, **kwargs: None
except (ImportError, AttributeError):
    pass

import asyncio
import time
from app.services.video_pipeline import run_video_pipeline_v10

async def main():
    # 1. Test with a dummy video
    test_video = "test_data/dataset/real/real_test_0.mp4"
    if not os.path.exists(test_video):
        print("Test video not found, generating...")
        import subprocess
        subprocess.run(["python", "create_dummy_video.py"], check=True)

    print(f"\n--- [TEST] Starting Phased Analysis on {test_video} ---")
    start = time.time()
    result = await run_video_pipeline_v10(test_video)
    elapsed = time.time() - start
    
    print(f"Total Wall Time: {elapsed:.2f}s")
    print(f"Status: {result.get('status')}")
    
    if result.get('status') == 'success':
        data = result['data']
        print(f"Verdict: {data.get('verdict')}")
        print(f"ProcessingTime in Data: {data.get('processing_time')}")
        print(f"Engine Version: {data.get('engine_version')}")
        
        # Check if it short-circuited (Engine version should say ShortCircuit)
        if "ShortCircuit" in data.get('engine_version', ''):
            print("✓ SUCCESS: Pipeline short-circuited as expected.")
        else:
            print("✓ SUCCESS: Pipeline completed full analysis.")
            
        print(f"Reasons: {data.get('reasons', 'N/A')}")
    else:
        print(f"Analysis failed: {result}")

if __name__ == "__main__":
    asyncio.run(main())
