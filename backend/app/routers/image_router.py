from fastapi import APIRouter, HTTPException, BackgroundTasks, Depends
from pydantic import BaseModel
from app.dependencies import verify_paid_tier
from app.routers.dashboard_router import save_scan_internal
# Model import moved inside endpoint for lazy loading
import base64
import io
import asyncio
import uuid
from typing import Dict, Any

class ImageAnalyzeRequest(BaseModel):
    image: str
    include_gradcam: bool = True

router = APIRouter(prefix="/api/v1/image", tags=["Image Lab"])


@router.post("/analyze")
async def analyze_image_endpoint(request: ImageAnalyzeRequest, user: dict = Depends(verify_paid_tier)):
    """
    Analyzes an image using the v2026 Forensic Truth Pipeline.
    Integrates RIGID (DINOv2), C2PA provenance, FFT, ELA, EXIF, and Multi-Neural Ensembles.
    """
    from app.models.image_detector import analyze_image
    try:
        image_data = request.image
        if not image_data:
            raise HTTPException(status_code=400, detail="No image data provided.")

        # Decode base64 image with sanitization
        if "," in image_data:
            _, encoded = image_data.split(",", 1)
        else:
            encoded = image_data

        # SANITIZATION: Strip whitespace/newlines and fix padding
        encoded = encoded.strip().replace(" ", "+").replace("\n", "").replace("\r", "")
        missing_padding = len(encoded) % 4
        if missing_padding:
            encoded += "=" * (4 - missing_padding)

        try:
            image_bytes = base64.b64decode(encoded)
        except Exception as e:
            raise HTTPException(
                status_code=400, detail=f"Invalid base64 image data: {str(e)}"
            )

        # ── MAGIC NUMBER VALIDATION ─────────────────────────────
        # Check for common image file signatures in the header bytes.
        # JPG: FF D8 FF | PNG: 89 50 4E 47 | WEBP/RIFF: 52 49 46 46 | BMP: 42 4D | TIFF: 49 49
        header = image_bytes[:12]
        is_valid = (
            header[:3] == b"\xff\xd8\xff"  # JPEG
            or header[:4] == b"\x89PNG"  # PNG
            or header[:4] == b"RIFF"  # WEBP
            or header[:3] == b"GIF"  # GIF
            or header[:2] == b"BM"  # BMP
            or header[:4] in (b"II*\x00", b"MM\x00*")  # TIFF
        )
        if not is_valid:
            # Check if it looks like HTML — use bytes comparison, NOT .lower() (bytes has no .lower())
            first_bytes = image_bytes[:64].decode("latin-1", errors="replace").lower()
            if "<!doc" in first_bytes or "<html" in first_bytes:
                raise HTTPException(
                    status_code=400,
                    detail="The forensic engine received an HTML document instead of an image. Ensure you are uploading a valid image file.",
                )
            raise HTTPException(
                status_code=400,
                detail="Unsupported or invalid image format. Please upload a valid JPG, PNG, or WEBP.",
            )

        # Run frontend-ready Image Forensics pipeline
        try:
            # analyze_image is synchronous and heavy, run it in a thread to keep the event loop alive
            result = await asyncio.to_thread(analyze_image, image_bytes, include_gradcam=request.include_gradcam)
            if "error" in result:
                raise ValueError(result["error"])
            
            # Persist to MongoDB
            try:
                verdict = "AI-Generated" if result.get("verdict") == 'AI GENERATED' else "Authentic" if result.get("verdict") == 'LIKELY HUMAN' else "Suspicious"
                prob = result.get("ai_probability", 0)
                await save_scan_internal(
                    email=user["email"],
                    lab="image",
                    filename="uploaded_image.png",
                    verdict=verdict,
                    confidence=prob,
                    threat_level="critical" if prob >= 0.72 else "high" if prob >= 0.5 else "low",
                    scan_id=f"img-{uuid.uuid4().hex[:8]}",
                    extra={
                        "verdict_raw": result.get("verdict"),
                        "ai_probability": prob,
                        "confidence": result.get("confidence")
                    },
                    full_result=result
                )
            except Exception as db_err:
                print(f"Failed to persist image scan to DB: {db_err}")

        except ValueError as ve:
            raise HTTPException(status_code=400, detail=str(ve))
        except Exception as e:
            import traceback

            traceback.print_exc()
            raise HTTPException(
                status_code=500, detail=f"Internal Forensic Crash: {str(e)}"
            )

        return {"status": "success", "data": result}

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        import traceback

        traceback.print_exc()
        raise HTTPException(
            status_code=500, detail=f"Forensic analysis crashed: {str(e)}"
        )
