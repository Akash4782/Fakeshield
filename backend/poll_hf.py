import time
from huggingface_hub import HfApi

api = HfApi()
repo_id = 'Akash4911/fakeshield-api'

print("Polling space status...")
for _ in range(60):  # Max 10 minutes
    try:
        runtime = api.get_space_runtime(repo_id)
        stage = runtime.stage
        print(f"[{time.strftime('%H:%M:%S')}] Stage: {stage}")
        if stage not in ('BUILDING', 'STARTING', 'RUNNING_BUILDING'):
            print(f"\nFinal stage: {stage}")
            if hasattr(runtime, 'raw') and runtime.raw.get('errorMessage'):
                print("Error:", runtime.raw['errorMessage'])
            break
        time.sleep(10)
    except Exception as e:
        print(f"Error: {e}")
        break
