from PIL import Image, ImageChops, ImageEnhance
import numpy as np
import io

def analyze_ela(img_pil: Image.Image, quality=90) -> tuple:
    """
    Error Level Analysis (ELA) detects compression discrepancies.
    AI images often display unnaturally uniform error levels across the grid.
    Real photos (with high detail/rough edges) exhibit uneven high-frequency errors.
    Returns: (float score 0-1, PIL.Image diff_visual)
    """
    try:
        # Step 1: Resave image at a lower JPEG quality
        # This creates a baseline recompression error
        buf = io.BytesIO()
        img_pil.convert('RGB').save(buf, format='JPEG', quality=quality)
        buf.seek(0)
        recomp = Image.open(buf)
        
        # Step 2: Compute absolute difference between original and recompressed
        # Regions with higher detail/noise have higher ELA values
        diff = ImageChops.difference(img_pil.convert('RGB'), recomp)
        
        # Multiply diff to enhance visualization (like in standard forensic tools)
        extrema = diff.getextrema()
        max_diff = max([ex[1] for ex in extrema])
        if max_diff == 0: max_diff = 1
        scale = 255.0 / max_diff
        
        enhanced_diff = ImageEnhance.Brightness(diff).enhance(scale)
        
        # Step 3: Statistical Score (Entropy/Variance)
        # AI images are generated from a single coherent latent pass.
        # This makes their compression 'layers' more uniform (lower variance).
        # Real camera images have sensor noise and complex textures.
        diff_arr = np.array(diff, dtype=float) / 255.0
        ela_score = np.mean(diff_arr)
        
        # High ELA score = potentially more details/forgeries
        # Very low ELA score = suspiciously smooth/AI-ish
        # We look for "flatness" (AI) vs "texture" (Real)
        # Normalization: 1.0 (Most AI-like/Flat) to 0.0 (Natural Texture)
        score = 1.0 - min(ela_score * 12.0, 1.0)
        
        return round(float(score), 4), enhanced_diff
    except Exception:
        return 0.5, None
