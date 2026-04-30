import os
import sys
import io
from PIL import Image
import numpy as np

# Add backend to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))

from app.models.image_detector import analyze_image

def create_test_image():
    # Create a 224x224 RGB image
    img = Image.fromarray(np.random.randint(0, 255, (224, 224, 3), dtype=np.uint8))
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    return buf.getvalue()

def test_v3_logic():
    print("Testing Image Detector v3.0...")
    image_bytes = create_test_image()
    
    try:
        report = analyze_image(image_bytes, include_gradcam=True)
        
        print("\nAnalysis Report Keys:")
        for key in report.keys():
            print(f"- {key}")
            
        print(f"\nVerdict: {report.get('verdict')}")
        print(f"Risk Score: {report.get('risk_score')}%")
        print(f"Confidence: {report.get('confidence')}%")
        print(f"Processing Time: {report.get('processing_time')}")
        
        # Check for expected schema fields
        expected_fields = [
            "signals", "signals_raw", "risk_score", "verdict", 
            "top_risk_factors", "reassuring_factors", "metadata_analysis",
            "gradcam_heatmap", "ela_image", "benchmark_proof"
        ]
        
        missing = [f for f in expected_fields if f not in report]
        if missing:
            print(f"\nWARNING: Missing expected fields: {missing}")
        else:
            print("\nSUCCESS: All expected schema fields present.")
            
    except Exception as e:
        print(f"\nFAILED: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_v3_logic()
