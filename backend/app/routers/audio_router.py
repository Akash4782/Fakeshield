# audio_router.py
import uuid
import logging
import asyncio
from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks, Depends
from app.dependencies import verify_paid_tier, get_current_user
from app.routers.dashboard_router import save_scan_internal
# Model import moved inside task for lazy loading

logger = logging.getLogger(__name__)
logger.info("Audio router initialized. Asyncio available: %s", "asyncio" in globals())

router = APIRouter(prefix="/audio", tags=["Audio Detection"])

# Expanded MIME type list — browsers are inconsistent about what they send
ALLOWED_TYPES = {
    "audio/wav",
    "audio/x-wav",
    "audio/wave",
    "audio/mpeg",
    "audio/mp3",
    "audio/mp4",
    "audio/flac",
    "audio/x-flac",
    "audio/ogg",
    "audio/vorbis",
    "audio/x-m4a",
    "audio/m4a",
    "audio/aac",
    "audio/webm",
    "video/mp4",        # some browsers send MP3s as video/mp4
    "video/webm",       # webm audio files
    "application/octet-stream",  # generic binary — fall through to extension check
}

ALLOWED_EXTENSIONS = {"wav", "mp3", "flac", "ogg", "m4a", "mp4", "aac", "webm"}
MAX_SIZE_MB = 50

job_store: dict = {}


def _get_extension(filename: str) -> str:
    if filename and "." in filename:
        return filename.rsplit(".", 1)[-1].lower()
    return ""


@router.post("/analyze/async")
async def analyze_async(
    file: UploadFile = File(...),
    background_tasks: BackgroundTasks = BackgroundTasks(),
    user: dict = Depends(verify_paid_tier)
):
    user_email = user["email"]
    filename = file.filename or "audio.wav"
    content_type = file.content_type or ""
    ext = _get_extension(filename)

    logger.info(f"Audio upload: filename={filename!r} content_type={content_type!r} ext={ext!r}")

    # Validate by content type OR by extension (browsers are inconsistent)
    type_ok = content_type in ALLOWED_TYPES
    ext_ok  = ext in ALLOWED_EXTENSIONS

    if not type_ok and not ext_ok:
        raise HTTPException(
            status_code=400,
            detail=(
                f"Unsupported audio format. "
                f"Got content_type={content_type!r}, extension=.{ext!r}. "
                f"Supported: WAV, MP3, FLAC, OGG, M4A"
            ),
        )

    audio_bytes = await file.read()

    if len(audio_bytes) == 0:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    if len(audio_bytes) > MAX_SIZE_MB * 1024 * 1024:
        raise HTTPException(
            status_code=413,
            detail=f"File too large ({len(audio_bytes) / 1024 / 1024:.1f}MB). Maximum is {MAX_SIZE_MB}MB.",
        )

    job_id = str(uuid.uuid4())
    job_store[job_id] = {"status": "processing", "filename": filename, "user_email": user_email}

    logger.info(f"Job created: {job_id} for {filename!r} ({len(audio_bytes)} bytes)")

    async def run():
        import asyncio
        from app.models.audio.audio_detector import analyze_audio
        try:
            # analyze_audio is synchronous and heavy, run it in a thread
            result = await asyncio.to_thread(analyze_audio, audio_bytes, filename)
            job_store[job_id] = {"status": "complete", "result": result}
            logger.info(f"Job complete: {job_id}")

            # Persist to MongoDB
            try:
                prob = result.get("ai_probability", 0)
                verdict = "AI-Generated" if prob > 65 else "Suspicious" if prob > 40 else "Authentic"
                await save_scan_internal(
                    email=user_email,
                    lab="audio",
                    filename=filename,
                    verdict=verdict,
                    confidence=prob / 100,
                    threat_level=result.get("threat_level", "low").lower(),
                    scan_id=f"aud-{uuid.uuid4().hex[:8]}",
                    extra={
                        "ai_probability": prob,
                        "confidence": result.get("confidence", "low"),
                        "agreement": result.get("agreement", "N/A")
                    },
                    full_result=result
                )
            except Exception as db_err:
                logger.error(f"Failed to persist audio scan to DB: {db_err}")

        except Exception as e:
            import traceback
            tb = traceback.format_exc()
            logger.error(f"Job failed: {job_id}\n{tb}")
            job_store[job_id] = {"status": "error", "error": str(e)}

    background_tasks.add_task(run)
    return {"job_id": job_id, "status": "processing"}


@router.get("/status/{job_id}")
def get_status(job_id: str, user: dict = Depends(get_current_user)):
    r = job_store.get(job_id)
    if not r:
        raise HTTPException(status_code=404, detail=f"Job '{job_id}' not found.")
    
    if r.get("user_email") != user["email"]:
        raise HTTPException(status_code=403, detail="Not authorized to view this job status")
        
    return r


@router.get("/health")
def health():
    return {
        "status": "ok",
        "system": "FakeShield Audio Lab v1.0",
        "signals": [
            "wavlm_itw",
            "ast_asvspoof5",
            "spectral_heuristics",
            "prosody_pitch_rhythm",
            "speaker_consistency_dual",
            "robustness_multipass",
        ],
        "requires": ["librosa", "soundfile", "transformers", "torch", "scipy"],
    }
