import os
import requests
from pathlib import Path

REAL_URLS = [
    ("portrait.jpg", "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=800&q=80"),
    ("architecture.jpg", "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?w=800&q=80"),
    ("nature.jpg", "https://images.unsplash.com/photo-1470071459604-3b5ec3a7fe05?w=800&q=80"),
    ("still_life.jpg", "https://images.unsplash.com/photo-1490818387583-1baba5e638af?w=800&q=80"),
    ("street.jpg", "https://images.unsplash.com/photo-1477959858617-67f85cf4f1df?w=800&q=80"),
]

AI_URLS = [
    ("ai_portrait.jpg", "https://lexica-serve-encoded-outputs.911-mks-east-1.algorithmic.media/out/0/02ff5a98-1819-47c8-8017-b7f4c3d928c7.jpg"),
    ("ai_architecture.jpg", "https://lexica-serve-encoded-outputs.911-mks-east-1.algorithmic.media/out/0/05a1d85f-9ba8-4804-b7c1-d93cd4b86695.jpg"),
    ("ai_nature.jpg", "https://lexica-serve-encoded-outputs.911-mks-east-1.algorithmic.media/out/0/c207a71b-38e7-45aa-89fd-75ed8314e47c.jpg"),
    ("ai_still_life.jpg", "https://lexica-serve-encoded-outputs.911-mks-east-1.algorithmic.media/out/0/0b7abf85-95d3-4bd6-aa69-e16b2dda959d.jpg"),
    ("ai_street.jpg", "https://lexica-serve-encoded-outputs.911-mks-east-1.algorithmic.media/out/0/00f261f5-5797-4167-b6f2-75d8b1a72dad.jpg"),
]

def download_dataset():
    Path("evaluation_dataset/real").mkdir(parents=True, exist_ok=True)
    Path("evaluation_dataset/ai").mkdir(parents=True, exist_ok=True)
    
    headers = {"User-Agent": "Mozilla/5.0"}
    
    print("Downloading Real Images...")
    for name, url in REAL_URLS:
        try:
            r = requests.get(url, headers=headers, timeout=10)
            if r.status_code == 200:
                with open(f"evaluation_dataset/real/{name}", "wb") as f:
                    f.write(r.content)
                print(f"  ✓ {name}")
            else:
                print(f"  ✗ {name} (Error {r.status_code})")
        except Exception as e:
            print(f"  ✗ {name} ({e})")

    print("\nDownloading AI Images...")
    for name, url in AI_URLS:
        try:
            r = requests.get(url, headers=headers, timeout=10)
            if r.status_code == 200:
                with open(f"evaluation_dataset/ai/{name}", "wb") as f:
                    f.write(r.content)
                print(f"  ✓ {name}")
            else:
                print(f"  ✗ {name} (Error {r.status_code})")
        except Exception as e:
            print(f"  ✗ {name} ({e})")

if __name__ == "__main__":
    download_dataset()
