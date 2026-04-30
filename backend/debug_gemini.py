import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
print(f"API Key found: {api_key[:10]}...")

if api_key:
    genai.configure(api_key=api_key)
    # Try multiple common model names for robustness
    models = ["gemini-2.0-flash-exp", "gemini-1.5-flash", "gemini-pro"]
    for model_name in models:
        try:
            print(f"Testing model: {model_name}")
            model = genai.GenerativeModel(model_name)
            response = model.generate_content("hello", generation_config={"max_output_tokens": 5})
            print(f"Success with {model_name}: {response.text}")
            break
        except Exception as e:
            print(f"Failed with {model_name}: {e}")
else:
    print("No API Key found in .env")
