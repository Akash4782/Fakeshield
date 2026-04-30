import requests
import base64

def test_html_input():
    # 1. Create a fake HTML "image" string
    html_data = "<!doctype html><html><body><h1>Fake Image</h1></body></html>"
    b64_data = base64.b64encode(html_data.encode('utf-8')).decode('utf-8')
    data_url = f"data:image/png;base64,{b64_data}"

    print(f"Sending HTML as image to backend...")
    
    try:
        response = requests.post(
            "http://localhost:8001/image/analyze",
            json={"image": data_url}
        )
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 400:
            print("SUCCESS: Backend correctly caught the HTML file with a 400 error.")
        else:
            print(f"FAILURE: Backend returned {response.status_code} instead of 400.")
            
    except Exception as e:
        print(f"Request failed: {e}")

if __name__ == "__main__":
    test_html_input()
