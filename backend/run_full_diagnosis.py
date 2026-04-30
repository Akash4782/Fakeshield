# run_full_diagnosis.py
import sys, os, torch
import torch.nn.functional as F
sys.path.append('.')
sys.path.append('..')

print("="*55)
print("  FakeShield Full System Diagnosis")
print("="*55)

# Test 1: Check what models are actually loaded
print("\n[1] Checking model loading...")
try:
    from app.models.text_detector import (
        ROBERTA_MODEL, ROBERTA_TOK, _AI_IDX,
        GPT2_MDL, GPT2_TOK
    )
    print(f"    ROBERTA_MODEL: {type(ROBERTA_MODEL).__name__} ✓")
    print(f"    _AI_IDX: {_AI_IDX}")
    print(f"    Labels: {ROBERTA_MODEL.config.id2label}")
    print(f"    GPT2: {type(GPT2_MDL).__name__} ✓")
except Exception as e:
    print(f"    ERROR: {e}")

# Test 2: Check label detection is correct
print("\n[2] Checking label correctness...")
try:
    labels = ROBERTA_MODEL.config.id2label
    print(f"    id2label: {labels}")
    for idx, name in labels.items():
        print(f"    Index {idx} = '{name}'")

    ai_text = (
        "Furthermore, it is important to note that machine learning "
        "represents a significant paradigm shift in computational "
        "intelligence. In conclusion, the implications are vast."
    )
    inputs  = ROBERTA_TOK(
        ai_text, return_tensors="pt",
        truncation=True, max_length=128, padding=True
    )
    outputs = ROBERTA_MODEL(**inputs)
    logits  = torch.tensor(outputs.logits) if not isinstance(outputs.logits, torch.Tensor) else outputs.logits
    probs   = F.softmax(logits, dim=-1).detach().numpy()[0]

    print(f"\n    Test on known AI text:")
    for idx, name in labels.items():
        print(f"    {name}: {round(float(probs[idx])*100,1)}%")
    print(f"\n    Using _AI_IDX={_AI_IDX}: {round(float(probs[_AI_IDX])*100,1)}%")

    if float(probs[_AI_IDX]) < 0.5:
        print("    *** LABEL MISMATCH DETECTED — scores are INVERTED ***")
    else:
        print("    Label detection: CORRECT ✓")

except Exception as e:
    print(f"    ERROR: {e}")

# Test 3: Run full analysis on the FULL screenshot text
print("\n[3] Running full analysis...")
try:
    from app.models.text_detector import analyze

    text = """Machine learning is a branch of Artificial Intelligence that enables 
computers to learn from data and improve their performance without being explicitly 
programmed for every task. Instead of following fixed rules, machine learning 
systems identify patterns and relationships within data, allowing them to make 
decisions or predictions. For example, email spam filters, recommendation systems, 
and voice assistants all rely on machine learning to function effectively.

At its core, machine learning works by using algorithms that process large amounts 
of data and build models based on that data. These models are trained using examples, 
which helps the system understand how to respond to new, unseen inputs. A key concept 
here is the idea of training and testing. During training, the model learns from 
known data, and during testing, it applies that knowledge to make predictions. 
The more relevant and high-quality data the system is given, the better it becomes 
at performing its task.

There are three main types of machine learning: supervised learning, unsupervised 
learning, and reinforcement learning. In supervised learning, the model is trained 
on labeled data, meaning each input comes with a correct answer. The model learns 
to map inputs to outputs based on these examples. This is the most common type 
and is used in tasks like email spam detection, image recognition, and price 
prediction.

Unsupervised learning, on the other hand, involves training on unlabeled data. 
The model must find patterns and structure on its own without any predefined answers. 
This approach is useful for tasks like customer segmentation, anomaly detection, 
and recommendation systems. Reinforcement learning is different from both. 
In this approach, an agent learns by interacting with an environment and receiving 
feedback in the form of rewards or penalties based on its actions."""

    result = analyze(text, include_highlights=False, mode="deep")

    print(f"\n    Results:")
    print(f"    Verdict:    {result['verdict']}")
    print(f"    Confidence: {result['confidence']}%")
    print(f"    Signals:")
    for k, v in result['signals'].items():
        print(f"      {k}: {v}%")

except Exception as e:
    print(f"    ERROR: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*55)
print("  Diagnosis complete")
print("="*55)
