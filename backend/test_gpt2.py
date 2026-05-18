import torch
import numpy as np
from transformers import GPT2LMHeadModel, AutoTokenizer

m_id = "gpt2-medium"
tok = AutoTokenizer.from_pretrained(m_id)
mdl = GPT2LMHeadModel.from_pretrained(m_id).eval()

def calculate_gpt2_stats(text: str):
    text_sample = " ".join(text.split()[:128])
    inputs = tok(text_sample, return_tensors="pt", truncation=True, max_length=256)
    with torch.no_grad():
        outputs = mdl(**inputs, labels=inputs["input_ids"])
        loss = outputs.loss
        perplexity = torch.exp(loss).item()
    
    tokens = inputs["input_ids"][0]
    chunk_size = 40
    chunks = []
    for i in range(0, len(tokens) - chunk_size, chunk_size):
        chunks.append(tokens[i:i+chunk_size])
    
    chunks = chunks[:3]
    
    if chunks:
        batched_chunks = torch.stack(chunks)
        with torch.no_grad():
            outputs = mdl(batched_chunks, labels=batched_chunks)
            logits = outputs.logits
            shift_logits = logits[..., :-1, :].contiguous()
            shift_labels = batched_chunks[..., 1:].contiguous()
            loss_fct = torch.nn.CrossEntropyLoss(reduction='none')
            loss = loss_fct(shift_logits.view(-1, shift_logits.size(-1)), shift_labels.view(-1))
            chunk_losses = loss.view(batched_chunks.size(0), -1).mean(dim=1).tolist()
    else:
        chunk_losses = []

    burstiness = np.var(chunk_losses) if chunk_losses else 0.0
    
    print("Chunks:", len(chunks))
    print("Chunk Losses:", chunk_losses)
    print("Variance (burstiness):", burstiness)
    print("Perplexity:", perplexity)
    
    # original logic
    if perplexity < 45:
        p_score = 1.0 - (max(perplexity, 18) - 18) / 54.0 
    else:
        p_score = max(0.0, 0.45 - (perplexity - 45) / 70.0)
    
    if burstiness < 0.10:
        b_score = 1.0 - (max(burstiness, 0.005) - 0.005) / 0.19
    else:
        b_score = max(0.0, 0.45 - (burstiness - 0.10) / 0.25)
        
    print(f"p_score: {p_score}, b_score: {b_score}")

text_ai = "As an artificial intelligence language model, I do not have personal feelings, beliefs, or desires. However, I can provide information and answer questions to the best of my knowledge and abilities based on my training data. Artificial intelligence is a rapidly growing field with many exciting applications in everyday life, from natural language processing to computer vision. We can see its impact across numerous sectors, such as healthcare, finance, and transportation."
print("AI TEXT:")
calculate_gpt2_stats(text_ai)

text_human = "The quick brown fox jumps over the lazy dog. Yesterday I was walking down the street when I saw a beautiful red car speeding by. I wondered where it was going so fast, maybe there was an emergency? Who knows. Anyway, I bought some milk at the grocery store and went home. The weather was quite chilly, so I made myself a cup of hot chocolate and watched a movie. It was a really relaxing evening after a long and exhausting day at work. I hope tomorrow brings better news."
print("\nHUMAN TEXT:")
calculate_gpt2_stats(text_human)
