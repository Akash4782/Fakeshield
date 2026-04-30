from app.models.modern_llm_detector import ModernLLMDetector

detector = ModernLLMDetector()

# Gemini-style technical text
gemini_text = """
**The Transformer Model**:
1. **Architecture**: It uses self-attention.
2. **Applications**: NLP, Vision.
In summary, it is worth noting that transformer models have redefined machine learning.
"""

# Human-style creative text
human_text = """
I was walking down the street when I saw a strange light. 
It wasn't a car, and it wasn't a plane. 
I wondered what it could be.
"""

print("Testing ModernLLMDetector:")
print("-" * 20)
print("AI Sample (Gemini style):")
res_ai = detector.detect(gemini_text)
print(res_ai)

print("\nHuman Sample:")
res_hu = detector.detect(human_text)
print(res_hu)
