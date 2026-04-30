import requests
import base64
import io
from PIL import Image

def test_endpoint():
    # 1. Create a tiny transparent image
    img = Image.new('RGBA', (1, 1), color=(0, 0, 0, 0))
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    b64_data = base64.b64encode(buf.getvalue()).decode('utf-8')
    data_url = f"data:image/png;base64,{b64_data}"

    print(f"Sending data URL: {data_url[:50]}...")
    
    try:
        response = requests.post(
            "http://localhost:8000/image/analyze",
            json={"image": data_url}
        )
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Request failed: {e}")

if __name__ == "__main__":
    test_endpoint()
