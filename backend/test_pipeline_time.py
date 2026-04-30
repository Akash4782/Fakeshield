import sys
import os
import asyncio
import time

# Ensure imports work regardless of execution location
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services.video_pipeline import run_video_pipeline_v10

async def main():
    test_video = "test_data/sample.mp4"
    if not os.path.exists(test_video):
        # find another test video
        for root, dirs, files in os.walk("test_data"):
            for f in files:
                if f.endswith(".mp4"):
                    test_video = os.path.join(root, f)
                    break
                    
    if not os.path.exists(test_video):
        # Even if temp, check temp dir just in case
        import glob
        test_video = next(iter(glob.glob(os.path.join(os.environ.get('TEMP', '/tmp'), '*.mp4'))), None)
        if not test_video:
            print("No test video found across known directories.")
            return

    print(f"Testing local execution speed for: {test_video}...")
    start = time.time()
    try:
        result = await run_video_pipeline_v10(test_video)
        elapsed = time.time() - start
        
        print(f"\n--- SUCCESS ---")
        print(f"Total True Pipeline Time: {elapsed:.2f} seconds")
        print(f"AI Models Engine Verdict: {result.get('data', {}).get('verdict', 'Unknown')}")
        print(f"Reported Backend Time: {result.get('data', {}).get('processing_time', 'Unknown')}")
    except Exception as e:
        print(f"Pipeline crashed: {e}")

if __name__ == "__main__":
    asyncio.run(main())
