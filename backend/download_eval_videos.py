# download_eval_videos.py
import urllib.request
import os

EVAL_DIR = "eval_samples"
os.makedirs(EVAL_DIR, exist_ok=True)

# Some reliable, small MP4 links from public GitHub deep-learning repos
DOWNLOADS = {
    "real_talking.mp4": "https://github.com/Rudrabha/Wav2Lip/raw/master/file/trim.mp4", 
    "ai_wav2lip_fake.mp4": "https://github.com/Rudrabha/Wav2Lip/raw/master/results/result_voice.mp4",
    "ai_first_order_fake.mp4": "https://github.com/AliaksandrSiarohin/first-order-model/raw/master/sup-mat/vox-demo.mp4",
    "ai_sora_like.mp4": "https://raw.githubusercontent.com/FurkanGozukara/Stable-Diffusion/main/Tutorials/Sora/sora-sample-1.mp4", # Fallback
    "ai_general_fake.mp4": "https://raw.githubusercontent.com/CorentinJ/Real-Time-Voice-Cloning/master/demo.mp4" # Often used for audio-sync fakes
}

def download_videos():
    print(f"📥 Downloading missing evaluation videos to {EVAL_DIR}/...")
    success_count = 0
    
    for filename, url in DOWNLOADS.items():
        filepath = os.path.join(EVAL_DIR, filename)
        if os.path.exists(filepath):
            print(f"✅ {filename} already exists.")
            success_count += 1
            continue
            
        print(f"   Downloading {filename}...")
        try:
            # Add headers to avoid 403 Forbidden on some raw GitHub/GitLab links
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=15) as response, open(filepath, 'wb') as out_file:
                out_file.write(response.read())
            print(f"   ✅ Saved {filename}")
            success_count += 1
        except Exception as e:
            print(f"   ❌ Failed to download {filename}: {e}")
            # If download fails, create a tiny blank video so the script doesn't crash 
            # (though it might fail face detection, it allows the rest of the eval loop to run)
            _create_dummy_video(filepath)

    print(f"\n🎉 Download complete. Successfully fetched {success_count}/{len(DOWNLOADS)} videos.")

def _create_dummy_video(filepath):
    """Fallback if internet blocks raw github links."""
    print(f"   ⚠️ Creating dummy fallback video for {filepath}...")
    import cv2
    import numpy as np
    out = cv2.VideoWriter(filepath, cv2.VideoWriter_fourcc(*'mp4v'), 30, (256, 256))
    for i in range(30): # 1 second
        frame = np.zeros((256, 256, 3), dtype=np.uint8)
        color = (0, 0, 255) if "ai" in filepath else (0, 255, 0)
        cv2.circle(frame, (128, 128), 50 + (i % 10), color, -1)
        out.write(frame)
    out.release()
    print(f"   ✅ Created dummy fallback {filepath}")

if __name__ == "__main__":
    download_videos()
