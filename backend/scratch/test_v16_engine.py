import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.models.new_forensic_engine import analyze_forensic, load_models

# Longer, more representative samples for v16 testing
AI_TEXT = (
    "Artificial intelligence (AI) has rapidly evolved from a theoretical concept to a transformative force "
    "reshaping modern society. At its core, AI involves the development of algorithms and systems capable "
    "of performing tasks that traditionally required human intelligence, such as visual perception, "
    "speech recognition, decision-making, and language translation. Furthermore, the advent of machine "
    "learning and deep neural networks has enabled computers to process vast amounts of data, identifying "
    "patterns and improving their performance over time. Moreover, generative AI models like Large Language "
    "Models (LLMs) have demonstrated an uncanny ability to produce human-like text, art, and even code. "
    "Consequently, this technology offers significant benefits across various sectors, including healthcare, "
    "finance, and transportation, by increasing efficiency and unlocking new possibilities. Nevertheless, "
    "the rapid deployment of AI also raises crucial ethical considerations regarding privacy, bias, and "
    "the future of work. In conclusion, while AI represents a pivotal shift in technological capability, "
    "a balanced approach is essential to ensure its development aligns with human values and societal well-being."
)

HUMAN_TEXT = (
    "I've been thinking a lot about AI lately, and honestly, it's a bit overwhelming. One minute you're "
    "reading about some amazing new medical breakthrough, and the next, everyone's worried about robots "
    "taking their jobs. I was talking to my brother about it yesterday, and he made a good point—technology "
    "always changes things, but people usually find a way to adapt. Still, it feels different this time. "
    "Like, when I saw that AI-generated video of a cat playing piano, I couldn't even tell it wasn't real "
    "at first. It's cool, but also kind of creepy, you know? I worry that we're moving too fast without "
    "really thinking about the consequences. We're so focused on what we *can* do that we forget to ask if "
    "we *should* do it. Anyway, I'm just rambling now. I think I'll go for a walk and clear my head. "
    "The real world still feels better than anything a screen can show me, at least for now."
)

def test():
    print("--- Loading Models v16 (Elite Forensic) ---")
    load_models()
    
    print("\n" + "="*50)
    print("ANALYZING AI GENERATED TEXT (GEMINI/GPT STYLE)")
    print("="*50)
    res_ai = analyze_forensic(AI_TEXT, mode="deep")
    print(f"Verdict:   {res_ai['verdict']}")
    print(f"Score:     {res_ai['score']}")
    print(f"DeBERTa:   {res_ai['signals']['classifier_signal']:.3f}")
    print(f"Bino:      {res_ai['signals']['binoculars_signal']:.3f}")
    print(f"PPL:       {res_ai['signals']['ppl_signal']:.3f}")
    print(f"Lexical:   {res_ai['signals']['lexical_signal']:.3f}")
    print(f"Reasoning: {res_ai['forensic_reasoning']}")
    
    print("\n" + "="*50)
    print("ANALYZING AUTHENTIC HUMAN TEXT")
    print("="*50)
    res_hum = analyze_forensic(HUMAN_TEXT, mode="deep")
    print(f"Verdict:   {res_hum['verdict']}")
    print(f"Score:     {res_hum['score']}")
    print(f"DeBERTa:   {res_hum['signals']['classifier_signal']:.3f}")
    print(f"Bino:      {res_hum['signals']['binoculars_signal']:.3f}")
    print(f"PPL:       {res_hum['signals']['ppl_signal']:.3f}")
    print(f"Lexical:   {res_hum['signals']['lexical_signal']:.3f}")
    print(f"Reasoning: {res_hum['forensic_reasoning']}")

if __name__ == "__main__":
    test()
