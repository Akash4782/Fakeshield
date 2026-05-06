import requests
from huggingface_hub import HfApi

import os
api = HfApi(token=os.getenv('HF_TOKEN'))
repo_id = 'Akash4911/fakeshield-api'

# Fetch logs - HF API provides logs via a specific endpoint
# Alternatively, we can try to get the errorMessage from runtime again
runtime = api.get_space_runtime(repo_id)
print(f"Stage: {runtime.stage}")
if hasattr(runtime, 'raw') and runtime.raw.get('errorMessage'):
    print(f"Error Message: {runtime.raw['errorMessage']}")

# Let's try to fetch the logs via requests if possible
# Or just check the build logs summary
