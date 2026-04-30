import os
import re

def clean_text(text: str) -> str:
    # 1. Remove emojis (basic range)
    # This regex covers many emoji ranges but not all. 
    # For a startup project, this is a solid first pass.
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)
    
    # 2. Remove weird formatting (extra spaces, newlines, etc.)
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    
    # 3. Basic normal sentence checking (ensure it ends with punctuation)
    # If it doesn't, we can add a period as a heuristic, but better to keep as is for benchmarking.
    
    return text

def clean_dataset(root_dir: str):
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".txt"):
                file_path = os.path.join(root, file)
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                
                cleaned = clean_text(content)
                
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(cleaned)
    print(f"Dataset cleaning complete for {root_dir}")

if __name__ == "__main__":
    clean_dataset("backend/dataset")
