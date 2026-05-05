import requests
import json
import time

API_BASE = "http://127.0.0.1:8001/api/v1/text"

def test_backend():
    print(f"Testing backend at {API_BASE}...")
    try:
        # 1. Check root
        res = requests.get("http://127.0.0.1:8001/")
        print(f"Root status: {res.status_code}")
        print(f"Root response: {res.json()}")

        # 2. Submit scan
        text = "This is a test sentence that should be long enough to be analyzed by the forensic engine. It needs to be at least twenty words long to avoid being rejected by the short text filter."
        print("\nSubmitting scan...")
        res = requests.post(f"{API_BASE}/analyze/async", json={
            "text": text,
            "mode": "deep"
        })
        print(f"Submit status: {res.status_code}")
        if res.status_code != 200:
            print(f"Submit error: {res.text}")
            return

        job_id = res.json().get("job_id")
        print(f"Job ID: {job_id}")

        # 3. Poll status
        for _ in range(10):
            print(f"Polling status for {job_id}...")
            res = requests.get(f"{API_BASE}/status/{job_id}")
            status_data = res.json()
            print(f"Status: {status_data.get('status')}")
            if status_data.get("status") == "complete":
                print("Scan complete!")
                # print(json.dumps(status_data.get("data"), indent=2))
                return
            elif status_data.get("status") == "error":
                print(f"Scan error: {status_data.get('data')}")
                return
            time.sleep(2)
        
        print("Timeout waiting for scan.")

    except Exception as e:
        print(f"Error connecting to backend: {e}")

if __name__ == "__main__":
    test_backend()
