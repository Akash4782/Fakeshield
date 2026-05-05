import os
from transformers import (
    AutoTokenizer, 
    AutoModelForSequenceClassification, 
    AutoModelForCausalLM,
    AutoImageProcessor,
    AutoModel,
    AutoModelForImageClassification,
    CLIPProcessor,
    CLIPModel,
    AutoFeatureExtractor,
    AutoModelForAudioClassification
)
from sentence_transformers import SentenceTransformer

def download():
    models = [
        # Text
        ("DmitryUv/deberta-v3-base-ai-text-detector", AutoModelForSequenceClassification),
        ("distilgpt2", AutoModelForCausalLM),
        ("EleutherAI/pythia-160m", AutoModelForCausalLM),
        ("EleutherAI/pythia-70m", AutoModelForCausalLM),
        
        # Image
        ("facebook/dinov2-base", AutoModel),
        ("umm-maybe/AI-image-detector", AutoModelForImageClassification),
        ("dima806/deepfake_vs_real_image_detection", AutoModelForImageClassification),
        ("openai/clip-vit-large-patch14", CLIPModel),
        
        # Audio
        ("abhishtagatya/wavlm-base-960h-itw-deepfake", AutoModelForAudioClassification),
        ("MattyB95/AST-ASVspoof5-Synthetic-Voice-Detection", AutoModelForAudioClassification),
    ]
    
    print("--- Starting Bulk Download of Forensic Models ---")
    
    for model_id, cls in models:
        print(f"\n[DOWNLOAD] {model_id}...")
        try:
            # Download tokenizer/processor
            if "clip" in model_id:
                CLIPProcessor.from_pretrained(model_id)
            elif "dinov2" in model_id or "image" in model_id or "deepfake" in model_id:
                AutoImageProcessor.from_pretrained(model_id)
            elif "wavlm" in model_id or "AST" in model_id:
                AutoFeatureExtractor.from_pretrained(model_id)
            else:
                AutoTokenizer.from_pretrained(model_id)
            
            # Download model
            cls.from_pretrained(model_id)
            print(f"      SUCCESS: {model_id}")
        except Exception as e:
            print(f"      FAILED: {model_id} - {e}")

    # Sentence Transformers
    st_models = ["all-mpnet-base-v2", "all-MiniLM-L6-v2"]
    for m in st_models:
        print(f"\n[DOWNLOAD] sentence-transformers/{m}...")
        try:
            SentenceTransformer(m)
            print(f"      SUCCESS: {m}")
        except Exception as e:
            print(f"      FAILED: {m} - {e}")

    print("\n--- All models verified/downloaded. ---")

if __name__ == "__main__":
    download()
