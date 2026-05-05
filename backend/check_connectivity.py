import requests
import sys

def check_service(name, url):
    try:
        response = requests.get(url, timeout=5)
        print(f"[OK] {name} is reachable at {url} (Status: {response.status_code})")
        return True
    except Exception as e:
        print(f"[FAIL] {name} is NOT reachable at {url}. Error: {e}")
        return False

if __name__ == "__main__":
    frontend_ok = check_service("Frontend", "http://127.0.0.1:5173")
    backend_ok = check_service("Backend", "http://127.0.0.1:8001/api/v1/text/status/health")
    
    # Check root as well
    backend_root = check_service("Backend Root", "http://127.0.0.1:8001/")
    
    if frontend_ok and backend_root:
        print("\nSUMMARY: Both services are active. The 'Failed to fetch' issue should be resolved by the auth patch.")
    else:
        print("\nSUMMARY: Connectivity issues detected. Check if servers are running.")
