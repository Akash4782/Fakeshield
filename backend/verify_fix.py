import requests
import base64
import json

def test_analyze():
    url = "http://localhost:8001/image/analyze"
    # Create a dummy image (1x1 white pixel)
    image_data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\x0cIDAT\x08\xd7c\xf8\xff\xff?1\xfe\x01\xfe\x01\xfe\x01\xbc3p\xcc\x00\x00\x00\x00IEND\xaeB`\x82'
    image_b64 = base64.b64encode(image_data).decode('utf-8')
    
    payload = {
        "image": image_b64,
        "include_gradcam": False
    }
    
    print(f"Sending request to {url}...")
    try:
        response = requests.post(url, json=payload, timeout=30)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            if "robustness" in data:
                print("SUCCESS: 'robustness' field found in response!")
                print(f"Robustness Data: {data['robustness']}")
                return True
            else:
                print("FAILURE: 'robustness' field missing from response!")
                print("Response Keys:", list(data.keys()))
                return False
        else:
            print(f"FAILURE: Server returned error {response.status_code}")
            print(response.text)
            return False
    except Exception as e:
        print(f"ERROR: {e}")
        return False

if __name__ == "__main__":
    test_analyze()
