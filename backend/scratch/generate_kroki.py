import base64
import zlib

def encode_kroki(text):
    compressed = zlib.compress(text.encode('utf-8'))
    return base64.urlsafe_b64encode(compressed).decode('utf-8')

m1 = '''graph TD
    A["Raw Text Input"] --> B{"Length Check >= 50 chars?"}
    B -- No --> C["Return Error: Too Short"]
    B -- Yes --> D["Concurrent Execution Trigger"]
    
    subgraph Primary Decision Layer
        D --> E["HC3 ChatGPT Detector<br>Hello-SimpleAI/chatgpt-detector-roberta"]
        D --> F["GPT-2 Medium<br>Statistical Engine"]
        
        E -->|"Sentence Avg 70% Weight"| G("Classifier Signal")
        F -->|"Perplexity 20% Weight"| H("Token Predictability")
        F -->|"Burstiness 10% Weight"| I("Token Variance")
    end
    
    subgraph Supplementary Layer
        D --> J["Forensic Structural Engine<br>spaCy"]
        J -->|"Tree Entropy, Cadence"| K["Structural Profile"]
        
        D --> L["Semantic Drift Engine<br>all-mpnet-base-v2"]
        L -->|"Thought Trajectory"| M["Semantic Profile"]
    end
    
    G & H & I --> P{"Calculate Base AI Probability"}
    P --> Q{"Is Mode='Deep' &<br>Score Uncertain? <br>0.42 to 0.62"}
    
    Q -- Yes --> R["LLM Forensic Judge"]
    R -->|"Analyzes Signals"| S["Adjusts Base Score<br>+/- 10%"]
    S --> T
    
    Q -- No --> T["Final AI Probability Score"]
    
    T --> U{"Threshold Evaluation"}
    U -->|"< 0.45"| V["LIKELY HUMAN"]
    U -->|"0.45 - 0.60"| W["UNCERTAIN"]
    U -->|"0.60 - 0.80"| X["LIKELY AI"]
    U -->|"> 0.80"| Y["AI GENERATED"]
    
    V & W & X & Y --> Z["Generate Final Report"]
    K & M -.-> Z'''

m2 = '''graph TD
    A(["Raw Text"]) --> B["Sentence Splitter"]
    B -->|"Filter length >= 5 words"| C["Valid Sentences Array"]
    C --> D["Batch Aggregator"]
    D -->|"Size = 8"| E["RoBERTa Tokenizer<br>Max Length 512"]
    E --> F["RoBERTa Classification Head"]
    F --> G["Logit Softmax"]
    G --> H["Extract AI Probability per Sentence"]
    H --> I["Calculate Simple Average"]
    H --> J["Calculate Weighted Average<br>Emphasizing High Confidence"]
    I & J --> K(["Final HC3 Document Score"])'''

m3 = '''graph TD
    A(["Raw Text"]) --> B["GPT-2 Fast Tokenizer"]
    B --> C{"Length > 350 Tokens?"}
    C -- No --> D["Single Tensor Input"]
    C -- Yes --> E["Sliding Window Chunking<br>Size: 350, Stride: 350"]
    
    D & E --> F["GPT-2 Medium Logits"]
    F --> G["Calculate Token Log-Probabilities"]
    
    G --> H["Calculate Mean<br>Log-Probs"]
    H -->|"exp-mean"| I["Perplexity Score"]
    
    G --> J["Calculate Variance<br>Log-Probs"]
    J --> K["Burstiness Score"]
    
    I --> L["Calibrated Sigmoid<br>Center: 32"]
    K --> M["Calibrated Sigmoid<br>Center: 1.8"]
    
    L --> N(["Perplexity AI Probability"])
    M --> O(["Burstiness AI Probability"])'''

m4 = '''graph TD
    A(["Raw Text"]) --> B["spaCy NLP Pipeline"]
    B --> C["Dependency Parsing Tree"]
    B --> D["Part-of-Speech Tagging"]
    
    C --> E["Calculate Depth Variance"]
    C --> F["Syntax Uniformity Check"]
    D --> G["Punctuation & Cadence Randomness"]
    
    E & F & G --> H{"Analyze Uniformity"}
    H -->|"High Uniformity"| I(["AI-like Clean Syntax"])
    H -->|"Lopsided/Irregular"| J(["Human-like Variance"])'''

m5 = '''graph TD
    A(["Raw Text"]) --> B["Sentence Splitter"]
    B --> C["SentenceTransformer Embeddings"]
    C --> D["Generate 768-D Vectors per Sentence"]
    
    D --> E["Compute Cosine Similarity<br>between adjacent sentences"]
    E --> F["Calculate Semantic Entropy"]
    E --> G["Calculate Vector Jumps / Drift"]
    
    F & G --> H{"Analyze Trajectory"}
    H -->|"Smooth, logical path"| I(["Geodesic AI Thought Flow"])
    H -->|"High variance, associative jumps"| J(["Natural Human Reasoning"])'''

m6 = '''graph TD
    A(["Uncertain Ensemble Score<br>0.42 - 0.62"]) --> B["Trigger Forensic Judge"]
    B --> C["Format LLM Prompt"]
    C -->|"Input"| D["Raw Text Data"]
    C -->|"Input"| E["Layer Breakdowns<br>HC3, PPL, Burstiness"]
    
    D & E --> F["LLM Inference"]
    F --> G["Extract Judge's AI Probability"]
    F --> H["Extract Forensic Reasoning"]
    F --> I["Extract Suspicious Indicators"]
    
    G --> J{"Judge Score vs Ensemble Score"}
    J -->|"Judge > 0.65 & Base < 0.60"| K["Adjust Base Score +10%"]
    J -->|"Judge < 0.35 & Base > 0.42"| L["Adjust Base Score -10%"]
    J -->|"Agree"| M["No Change"]
    
    K & L & M --> N(["Final Calibrated Probability"])
    H & I -.-> O(["Report Metadata"])'''

with open('c:/Users/office/Documents/Final_year_project/backend/scratch/kroki_urls.txt', 'w') as f:
    f.write('url1 = "https://kroki.io/mermaid/svg/' + encode_kroki(m1) + '"\n')
    f.write('url2 = "https://kroki.io/mermaid/svg/' + encode_kroki(m2) + '"\n')
    f.write('url3 = "https://kroki.io/mermaid/svg/' + encode_kroki(m3) + '"\n')
    f.write('url4 = "https://kroki.io/mermaid/svg/' + encode_kroki(m4) + '"\n')
    f.write('url5 = "https://kroki.io/mermaid/svg/' + encode_kroki(m5) + '"\n')
    f.write('url6 = "https://kroki.io/mermaid/svg/' + encode_kroki(m6) + '"\n')
