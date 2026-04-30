import os
import urllib.request

def download_samples():
    print("Downloading sample dataset for V28 Calibration...")
    
    # Create directories
    real_dir = "test_data/dataset/real"
    ai_dir = "test_data/dataset/ai"
    os.makedirs(real_dir, exist_ok=True)
    os.makedirs(ai_dir, exist_ok=True)
    
    # 1. Real videos (Standard test clips from Google storage)
    real_urls = [
        "http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4",
        "http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerEscapes.mp4"
    ]
    
    # 2. AI videos 
    # For testing, we'll download some known synthetic/CGI test videos 
    # (Since direct URLs to raw Sora/HeyGen outputs are ephemeral, we use reliable CGI/Blender tests as a proxy for "synthetic" content)
    ai_urls = [
        "http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ElephantsDream.mp4",
        "http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/Sintel.mp4" 
    ]
    
    for i, url in enumerate(real_urls):
        path = os.path.join(real_dir, f"real_test_{i}.mp4")
        if not os.path.exists(path):
            print(f"Downloading {url} to {path}...")
            try:
                urllib.request.urlretrieve(url, path)
            except Exception as e:
                print(f"Failed to download {url}: {e}")
                
    for i, url in enumerate(ai_urls):
        path = os.path.join(ai_dir, f"ai_test_{i}.mp4")
        if not os.path.exists(path):
            print(f"Downloading {url} to {path}...")
            try:
                urllib.request.urlretrieve(url, path)
            except Exception as e:
                print(f"Failed to download {url}: {e}")
                
    print("Done downloading sample dataset.")

if __name__ == "__main__":
    download_samples()
