import cv2
import numpy as np
import os

def generate_video(filename, width=320, height=240, frames=16, is_ai=False):
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(filename, fourcc, 15.0, (width, height))
    
    for i in range(frames):
        # Create a basic frame
        frame = np.zeros((height, width, 3), dtype=np.uint8)
        
        if is_ai:
            # Add synthetic-looking noise and sharp edges (Deepfake artifact simulation)
            noise = np.random.normal(0, 15, (height, width, 3)).astype(np.uint8)
            frame = cv2.add(frame, noise)
            # Add a moving sharp square
            cv2.rectangle(frame, (i*10, height//2 - 20), (i*10 + 40, height//2 + 20), (255, 0, 0), -1)
        else:
            # Simulate real camera (smooth motion, natural blur)
            base_color = min(255, 100 + i*5)
            frame[:] = (base_color, base_color, base_color)
            # Add a moving circle
            cv2.circle(frame, (width//2 + int(np.sin(i/2.0)*30), height//2), 20, (0, 255, 0), -1)
            # Apply slight blur
            frame = cv2.GaussianBlur(frame, (5, 5), 0)
            
        out.write(frame)
        
    out.release()
    print(f"Created {filename}")

os.makedirs("test_data/dataset/real", exist_ok=True)
os.makedirs("test_data/dataset/ai", exist_ok=True)

generate_video("test_data/dataset/real/real_test_0.mp4", is_ai=False)
generate_video("test_data/dataset/real/real_test_1.mp4", is_ai=False)
generate_video("test_data/dataset/ai/ai_test_0.mp4", is_ai=True)
generate_video("test_data/dataset/ai/ai_test_1.mp4", is_ai=True)
