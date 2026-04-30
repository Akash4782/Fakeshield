import torch
import torch.nn as nn
from transformers import RobertaModel, RobertaTokenizer, DebertaV2ForSequenceClassification, AutoTokenizer, DebertaV2Config
from safetensors.torch import load_file

class SuperAnnotateDetector(nn.Module):
    def __init__(self):
        super().__init__()
        self.roberta = RobertaModel.from_pretrained("roberta-large")
        self.classifier = nn.Linear(1024, 1)
        
    def forward(self, input_ids, attention_mask=None):
        out = self.roberta(input_ids=input_ids, attention_mask=attention_mask)
        # Use simple CLS token (index 0)
        cls_output = out.last_hidden_state[:, 0, :]
        logits = self.classifier(cls_output)
        return logits

def load_superannotate():
    print("Loading SA...")
    model = SuperAnnotateDetector()
    
    sd = load_file(r'C:\Users\office\.cache\huggingface\hub\models--SuperAnnotate--ai-detector\snapshots\74b2b8580915c202607c09f64f8170eaa87a6a14\model.safetensors')
    
    new_sd = {}
    for k, v in sd.items():
        if k == 'dense.weight':
            new_sd['classifier.weight'] = v
        elif k == 'dense.bias':
            new_sd['classifier.bias'] = v
        else:
            new_sd[k] = v
            
    # Fix missing position_ids if needed
    if "roberta.embeddings.position_ids" in model.state_dict() and "roberta.embeddings.position_ids" not in sd:
        new_sd["roberta.embeddings.position_ids"] = model.state_dict()["roberta.embeddings.position_ids"]
        
    model.load_state_dict(new_sd, strict=False)
    model.eval()
    
    tok = RobertaTokenizer.from_pretrained("SuperAnnotate/ai-detector")
    enc = tok("Furthermore, machine learning represents a significant paradigm shift.", return_tensors="pt")
    with torch.no_grad():
        logits = model(**enc)
        score = torch.sigmoid(logits).item()
        print(f"SA Score (expected high if AI): {score}")

def load_desklib():
    print("Loading desklib...")
    config = DebertaV2Config.from_pretrained("desklib/ai-text-detector-v1.01")
    model = DebertaV2ForSequenceClassification(config)
    
    sd = load_file(r'C:\Users\office\.cache\huggingface\hub\models--desklib--ai-text-detector-v1.01\snapshots\5fdea974cd4287c61674951ec78803aa274e2fb7\model.safetensors')
    
    new_sd = {}
    for k, v in sd.items():
        if k.startswith('model.'):
            new_sd[k.replace('model.', 'deberta.', 1)] = v
        else:
            new_sd[k] = v
            
    model.load_state_dict(new_sd, strict=False)
    model.eval()
    
    tok = AutoTokenizer.from_pretrained("desklib/ai-text-detector-v1.01")
    enc = tok("Furthermore, machine learning represents a significant paradigm shift.", return_tensors="pt")
    with torch.no_grad():
        out = model(**enc)
        probs = torch.nn.functional.softmax(out.logits, dim=-1).numpy()[0]
        # In desklib, usually label 1 is AI (FAKE)
        score = probs[1] if len(probs)>1 else probs[0]
        print(f"Desklib FAKE Probs: {score}")

if __name__ == "__main__":
    load_superannotate()
    load_desklib()
