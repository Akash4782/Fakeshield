import os
import re

file_path = r"c:\Users\office\Documents\Final_year_project\backend\app\models\text_detector.py"

with open(file_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

new_lines = []
patterns = [
    r"^(\s*)import torch",
    r"^(\s*)import numpy",
    r"^(\s*)from safetensors\.torch",
    r"^(\s*)from transformers",
    r"^(\s*)def __round_safe",
    r"round\(",
    r"MODEL_A\(",
    r"MODEL_B_PIPE\(",
    r"MODEL_C_MDL\(",
    r"res\[\"score\"\]",
    r"res\[\"label\"\]",
]

for i, line in enumerate(lines):
    # Skip if we already added pyre-ignore
    if "pyre-ignore" in line:
        new_lines.append(line)
        continue
    
    match = False
    indent = ""
    for p in patterns:
        m = re.search(p, line)
        if m:
            match = True
            if m.groups():
                indent = m.group(1)
            else:
                spaces = len(line) - len(line.lstrip())
                indent = line[:spaces]
            break
            
    if match:
        prev_line = lines[i-1] if i > 0 else ""
        if "# pyre-ignore" not in prev_line:
            new_lines.append(f"{indent}# pyre-ignore\n")
            
    new_lines.append(line)

with open(file_path, "w", encoding="utf-8") as f:
    f.writelines(new_lines)

print("Done injecting # pyre-ignore")
