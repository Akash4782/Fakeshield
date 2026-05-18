import google.generativeai as genai
from app.config import settings
import json
import re

class ForensicJudge:
    """
    ForensicJudge v10.0 (Core Reasoning Intelligence)
    Promoted from 'explainer' to 'primary forensic analyzer'.
    Uses the 2026 'Industrial Master Brain' prompt for behavior-based detection.
    """

    def __init__(self, api_key: str = None):
        api_key = api_key or settings.GEMINI_API_KEY
        self.enabled = False
        if api_key:
            genai.configure(api_key=api_key)
            # Build model list: Priority from settings + hardcoded fallbacks
            # We use names verified for 2026-era SDKs and legacy fallbacks
            model_list = [
                "gemini-1.5-flash", 
                "gemini-1.5-pro", 
                "gemini-1.5-flash-8b",
                "gemini-2.0-flash", 
                "gemini-3.1-pro-preview", 
                "gemini-3-flash-preview"
            ]
            if settings.GEMINI_MODEL:
                # Clean up name if it has aliases (e.g. "Gemini 3 Flash" -> "gemini-3-flash-preview")
                preferred = settings.GEMINI_MODEL.lower().replace(" ", "-")
                if "gemini-3-flash" in preferred: preferred = "gemini-3-flash-preview"
                
                if preferred not in model_list:
                    model_list.insert(0, preferred)
                else:
                    model_list.remove(preferred)
                    model_list.insert(0, preferred)

            for model_name in model_list:
                try:
                    # Fix: Ensure model names are correctly formatted for the SDK
                    # Some environments require 'models/' prefix, others don't. 
                    # We try the raw name first as it's the 2026 standard.
                    self.model = genai.GenerativeModel(model_name)
                    # Real verification: Dummy call (short)
                    self.model.generate_content("ok", generation_config={"max_output_tokens": 1})
                    self.enabled = True
                    self.active_model = model_name
                    print(f"[ForensicJudge v10] Initialized with {model_name}")
                    break
                except Exception as e:
                    err_str = str(e)
                    # If we get a 429 (Quota), the model EXISTS and the key is VALID.
                    # However, we should try to find another model that ISN'T rate limited first.
                    if "429" in err_str or "quota" in err_str.lower():
                        print(f"[ForensicJudge] {model_name} is currently rate-limited (429). Trying fallbacks...")
                        if not hasattr(self, 'fallback_model'):
                            self.fallback_model = model_name
                        continue
                    
                    # If we get a 404, the model name might need a prefix or is unavailable
                    if "404" in err_str:
                        alt_name = f"models/{model_name}" if not model_name.startswith("models/") else model_name.replace("models/", "")
                        try:
                            self.model = genai.GenerativeModel(alt_name)
                            self.model.generate_content("ok", generation_config={"max_output_tokens": 1})
                            self.enabled = True
                            self.active_model = alt_name
                            print(f"[ForensicJudge v10] Initialized with {alt_name} (via prefix fallback)")
                            break
                        except:
                            pass # Still failed, move to next model in list
                    
                    print(f"[ForensicJudge] Debug: Skipping {model_name} due to error: {err_str[:100]}...")
                    continue
            
            # If no model worked perfectly but we found a rate-limited one, use it as fallback
            if not self.enabled and hasattr(self, 'fallback_model'):
                self.enabled = True
                self.is_rate_limited = True
                self.active_model = self.fallback_model
                self.model = genai.GenerativeModel(self.active_model)
                print(f"[ForensicJudge v10] Initialized with {self.active_model} (Status: Rate Limited/Quota Mode)")
        
        if not hasattr(self, 'is_rate_limited'):
            self.is_rate_limited = False

        
        if not self.enabled:
            print("[ForensicJudge] Warning: Reasoning Engine DISABLED (API Key or Model Issue).")
            print("[ForensicJudge] Check GEMINI_API_KEY in .env and verify model availability.")

    def evaluate_text(self, text: str, metrics: dict = None) -> dict:
        """
        Performs a deep forensic audit and returns a reasoning score + JSON data.
        Reviews raw text alongside layer scores (HC3, Perplexity, Burstiness).
        """
        if not self.enabled:
            return {"ai_probability": 0.5, "verdict": "Uncertain", "reasoning": "Judge offline.", "suspicious_indicators": []}

        if metrics is None: metrics = {}

        # v14.0 Forensic Judge Brain (Researcher-Grade)
        prompt = f"""
You are an expert Forensic AI Judge (Version 14.0).
Your task is to provide a final ruling on a text sample that has returned "Uncertain" results in automated ensemble testing.

TEXT SAMPLE (First 2500 chars):
\"\"\"{text[:2500]}\"\"\"

CORE ENSEMBLE SIGNALS:
- HC3 ChatGPT Detector Score: {metrics.get('hc3_score', 'N/A')}
- Perplexity Signal: {metrics.get('perplexity', 'N/A')}
- Burstiness Signal: {metrics.get('burstiness', 'N/A')}

YOUR MANDATE:
1. Review the "Linguistic DNA": Look for robotic perfection, uniform rhythm, and "Explain-o-matic" structure (Intro -> Mechanism -> Summary).
2. Look for "Human Friction": Organic topic jumps, irregular punctuation, and associative reasoning that AI typically lacks.
3. Provide a final probability adjustment.

OUTPUT FORMAT (STRICT JSON ONLY):
{{
  "ai_probability": (0.0-1.0),
  "verdict": "LIKELY AI" | "UNCERTAIN" | "LIKELY HUMAN" | "AI GENERATED",
  "reasoning": "Direct forensic evidence summary.",
  "suspicious_indicators": ["List", "of", "indicators"]
}}
"""
        try:
            response = self.model.generate_content(
                prompt, 
                generation_config={"response_mime_type": "application/json"}
            )
            clean_text = re.sub(r'```json\s*|\s*```', '', response.text.strip())
            data = json.loads(clean_text)
            return data
        except Exception as e:
            print(f"[ForensicJudge] Evaluation failed: {e}")
            return {"ai_probability": 0.5, "verdict": "UNCERTAIN", "reasoning": "Analysis failed due to engine latency."}

    def evaluate(self, text: str, metrics: dict) -> dict:
        return self.evaluate_text(text, metrics)

    def explain(self, text: str, metrics: dict, verdict: str) -> str:
        """Generates a professional forensic explanation (Legacy support/UI display)."""
        if not self.enabled:
            return "Forensic reasoning unavailable."
            
        # Re-using evaluate for better consistency in v10
        evaluation = self.evaluate(text, metrics)
        return f"Forensic Analysis: {evaluation.get('reasoning', 'Analysis complete.')}"
