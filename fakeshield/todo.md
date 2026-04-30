# FakeShield v16 Upgrade Plan

## Completed
- [x] Research latest 2024-2025 AI detection approaches (Ghostbuster, Binoculars, DivEye).
- [x] Replace HC3 with **DeBERTa-v3-base** for better transformer-level detection.
- [x] Replace GPT-2 Medium with **DistilGPT2** for faster CPU-based statistical analysis.
- [x] Integrate **Binoculars** (Cross-Perplexity) into the ensemble scoring (Weight: 20%).
- [x] Implement **DivEye** inspired signals (Surprisal Variance / Rhythmic Analysis).
- [x] Update **Forensic Engine v16** with Adaptive Fusion and refined thresholds.

## Next Steps
- [ ] Optimize model loading with lazy-loading and threading.
- [ ] Implement **ONNX** runtime for DeBERTa to improve CPU inference speed.
- [ ] Fine-tune DeBERTa-v3 on a mixed dataset of Gemini 1.5, Claude 3.5, and Human text.
- [ ] Expand the **Lexical Scorer** patterns for 2026-era LLM "tells."
- [ ] Add "Style Transfer" detection (detecting when AI tries to mimic a specific human style).
