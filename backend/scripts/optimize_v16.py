import os
from optimum.onnxruntime import ORTModelForSequenceClassification
from transformers import AutoTokenizer

def optimize_neural_model():
    model_id = "Hello-SimpleAI/chatgpt-detector-roberta"
    save_dir = "pt_models/onnx_neural"
    
    print(f"--- Optimizing {model_id} for CPU ---")
    
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
        
    print("[1/3] Exporting to ONNX...")
    # This exports to ONNX and also performs graph optimization (operator fusion, etc.)
    model = ORTModelForSequenceClassification.from_pretrained(
        model_id, 
        export=True
    )
    
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    
    print("[2/3] Saving Optimized Model...")
    model.save_pretrained(save_dir)
    tokenizer.save_pretrained(save_dir)
    
    print(f"[3/3] DONE! Optimized model saved to {save_dir}")
    print("\nNote: Quantization to INT8 would require a calibration dataset.")
    print("For now, this FP32 optimized ONNX will already give a significant speedup on CPU.")

if __name__ == "__main__":
    optimize_neural_model()
