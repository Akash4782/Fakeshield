import requests
import time

text = """
Artificial Intelligence has made significant strides in recent years. Moreover, it has transformed various industries. 
Furthermore, the integration of LLMs allows for seamless communication. At its core, the technology is fundamentally 
different from traditional systems. In essence, it leverages robust frameworks to unlock the full potential of data. 
In conclusion, AI will continue to elevate the technological landscape.
"""

print("Submitting job...")
r = requests.post('http://localhost:8001/api/v1/text/analyze/async', json={'text': text})
print(f"Submission: {r.json()}")
job_id = r.json()['job_id']

print("Polling for error...")
for _ in range(20):
    res = requests.get(f'http://localhost:8001/api/v1/text/status/{job_id}').json()
    print(f"Status: {res['status']}")
    if res['status'] == 'error':
        print(f"ERROR FOUND: {res['data']}")
        break
    if res['status'] == 'complete':
        print("Success (unexpected)")
        break
    time.sleep(1)
