import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification, GPT2LMHeadModel, GPT2Tokenizer
import numpy as np
import os

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

def test_model(model_name, text):
    print(f"\nTesting {model_name}...")
    try:
        tok = AutoTokenizer.from_pretrained(model_name)
        if "gpt2" in model_name:
            mdl = GPT2LMHeadModel.from_pretrained(model_name).to(DEVICE)
        else:
            mdl = AutoModelForSequenceClassification.from_pretrained(model_name).to(DEVICE)
        mdl.eval()
        
        inputs = tok(text, return_tensors="pt", truncation=True, max_length=512).to(DEVICE)
        with torch.no_grad():
            outputs = mdl(**inputs, labels=inputs["input_ids"]) if "gpt2" in model_name else mdl(**inputs)
        
        if "gpt2" in model_name:
            loss = outputs.loss.item()
            print(f"   PPL: {np.exp(loss):.2f}")
        else:
            probs = torch.softmax(out.logits, dim=1)[0].tolist() if 'out' in locals() else torch.softmax(outputs.logits, dim=1)[0].tolist()
            print(f"   Probs: {probs}")
            print(f"   Labels: {mdl.config.id2label}")
    except Exception as e:
        print(f"   Error: {e}")

human_text = "Climate change, a significant global challenge, refers to long-term shifts in weather patterns..."
ai_text = "Artificial intelligence is a branch of computer science that deals with the creation of intelligent agents..."

test_model("Hello-SimpleAI/chatgpt-detector-roberta", human_text)
test_model("Hello-SimpleAI/chatgpt-detector-roberta", ai_text)
test_model("gpt2", human_text)
test_model("gpt2", ai_text)
