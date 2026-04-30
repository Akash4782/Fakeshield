import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("NO_KEY")
    exit()

genai.configure(api_key=api_key)
# Just test one reliable model
try:
    model = genai.GenerativeModel("gemini-1.5-flash")
    res = model.generate_content("ok", generation_config={"max_output_tokens": 1})
    print(f"SUCCESS_{model.model_name}")
except Exception as e:
    print(f"FAILED: {e}")
