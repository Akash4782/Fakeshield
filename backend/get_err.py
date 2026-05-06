import json
from huggingface_hub import HfApi
with open('error_out.txt', 'w', encoding='utf-8') as f:
    f.write(json.dumps(HfApi().get_space_runtime('Akash4911/fakeshield-api').raw))
