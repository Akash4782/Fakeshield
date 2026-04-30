# debug_s4.py
import sys, os, math, torch
import torch.nn.functional as F
sys.path.append(os.path.join(os.getcwd(), "backend"))

from app.models.text_detector import GPT2_TOK, GPT2_MDL

text = """Machine Learning is a subfield of Artificial Intelligence that focuses 
on enabling computers to learn from data and improve their performance without 
being explicitly programmed. Instead of relying on fixed rules, machine learning 
systems adapt by identifying patterns and making decisions based on past experiences.
This makes them highly flexible and capable of handling complex tasks."""

enc = GPT2_TOK(
    text, return_tensors="pt", truncation=True, max_length=256
)
with torch.no_grad():
    logits = GPT2_MDL(**enc).logits
    log_p  = F.log_softmax(logits, dim=-1)
    ids    = enc["input_ids"][0]
    tok_lp = log_p[0, range(len(ids)-1), ids[1:]]

mean_lp = tok_lp.mean().item()
var_lp  = tok_lp.var().item()
med_lp  = tok_lp.median().item()
hc      = (tok_lp > -2.0).float().mean().item()
vhc     = (tok_lp > -1.0).float().mean().item()

print(f"mean_lp   = {round(mean_lp, 6)}")
print(f"median_lp = {round(med_lp,  6)}")
print(f"var_lp    = {round(var_lp,  6)}")
print(f"high_conf (>-2.0) = {round(hc,  4)}")
print(f"very_high (>-1.0) = {round(vhc, 4)}")

# Show distribution
vals = tok_lp.tolist()
print(f"\nMin:    {round(min(vals),3)}")
print(f"Max:    {round(max(vals),3)}")
print(f"Tokens > -1.0: {sum(1 for v in vals if v > -1.0)}")
print(f"Tokens > -2.0: {sum(1 for v in vals if v > -2.0)}")
print(f"Tokens > -3.0: {sum(1 for v in vals if v > -3.0)}")
print(f"Tokens < -5.0: {sum(1 for v in vals if v < -5.0)}")
print(f"Total tokens:  {len(vals)}")
