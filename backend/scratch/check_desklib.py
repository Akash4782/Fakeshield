import torch
from transformers import AutoTokenizer, DebertaV2Config, DebertaV2ForSequenceClassification
from huggingface_hub import hf_hub_download
from safetensors.torch import load_file

MODEL = "desklib/ai-text-detector-v1.01"
tokenizer = AutoTokenizer.from_pretrained(MODEL)
config = DebertaV2Config.from_pretrained(MODEL, num_labels=1)
model = DebertaV2ForSequenceClassification(config)
sd_path = hf_hub_download(MODEL, "model.safetensors")
sd = load_file(sd_path)
new_sd = { (k.replace('model.', 'deberta.', 1) if k.startswith('model.') else k): v for k, v in sd.items() }
model.load_state_dict(new_sd, strict=False)
model.eval()

text_human = "Honestly, I think we should just go for pizza because it's easier for everyone."
text_ai = "In conclusion, the multifaceted benefits of artificial intelligence are significant in the modern landscape."

def get_score(text):
    inputs = tokenizer(text, return_tensors="pt")
    with torch.no_grad():
        out = model(**inputs)
    # The config has num_labels=1, so it might be a regressor/sigmoid 
    # or the code in new_forensic_engine.py handles it.
    # In new_forensic_engine.py:
    # if probs3.shape[0] >= 2: s3 = float(probs3[1].item())
    # else: s3 = float(torch.sigmoid(out.logits[0][0]).item())
    
    logits = out.logits
    if logits.shape[1] >= 2:
        probs = torch.softmax(logits, dim=1)[0]
        return probs[1].item()
    else:
        return torch.sigmoid(logits[0][0]).item()

print(f"Human score (AI prob): {get_score(text_human)}")
print(f"AI score (AI prob): {get_score(text_ai)}")
