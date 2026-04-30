import re
import subprocess
import os

# Read the markdown file
with open('ai_image_lab_architecture.md', 'r', encoding='utf-8') as f:
    content = f.read()

# Find all mermaid blocks
mermaid_pattern = r'```mermaid\n(.*?)\n```'
matches = re.findall(mermaid_pattern, content, re.DOTALL)

# For each match, save to temp file, convert to svg, replace in content
for i, match in enumerate(matches):
    # Save to temp.mmd
    with open(f'temp{i}.mmd', 'w', encoding='utf-8') as f:
        f.write(match)
    
    # Convert to svg
    subprocess.run(['powershell', '-File', 'C:\\Users\\office\\AppData\\Roaming\\npm\\mmdc.ps1', '-i', f'temp{i}.mmd', '-o', f'diagram{i}.svg'])
    
    # Replace in content
    content = content.replace(f'```mermaid\n{match}\n```', f'<img src="diagram{i}.svg" alt="Diagram {i}">')

# Write the modified content to new md
with open('ai_image_lab_architecture_modified.md', 'w', encoding='utf-8') as f:
    f.write(content)

# Clean up temp files
for i in range(len(matches)):
    os.remove(f'temp{i}.mmd')