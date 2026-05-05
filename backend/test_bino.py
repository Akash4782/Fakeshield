from app.models.binoculars import Binoculars

b = Binoculars()

human_text = "I went to the store today and bought some apples. It was a nice day." * 10
ai_text = "The implementation of neural networks in modern data analytics underscores the importance of scalable infrastructure." * 10

print("\n--- BINOCULARS TEST ---")
for text, label in [(human_text, "HUMAN"), (ai_text, "AI")]:
    res = b.predict(text)
    print(f"[{label}] Score: {res['score']}, Prob: {res['ai_probability']}")
