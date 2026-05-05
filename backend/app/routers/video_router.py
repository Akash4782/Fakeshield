import os
import uuid
import shutil
import tempfile
import asyncio
from fastapi import APIRouter, HTTPException, BackgroundTasks, UploadFile, File, Depends
from app.dependencies import verify_paid_tier
from app.routers.dashboard_router import save_scan_internal
# Pipeline import moved inside endpoint for lazy loading

router = APIRouter(prefix="/video", tags=["Video Forensics"])

# In-memory job store
_jobs = {}

@router.post("/analyze/async")
async def analyze_video_async(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    user: dict = Depends(verify_paid_tier)
):
    """
    Async video analysis v10.0. Uploads file, starts background task, returns job_id.
    """
    job_id = "v10_" + str(uuid.uuid4())[:8]
    user_email = user["email"]
    filename = file.filename or "video.mp4"
    _jobs[job_id] = {"status": "processing", "result": None, "user_email": user_email}

    # Create a persistent temp file
    fd, temp_path = tempfile.mkstemp(suffix=os.path.splitext(file.filename)[1])
    os.close(fd)

    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    async def run_analysis():
        from app.services.video_pipeline import run_video_pipeline_v10
        try:
            # Run the v10.0 Consistency Engine analysis
            report = await run_video_pipeline_v10(temp_path)
            _jobs[job_id] = {**report, "status": "complete"}
            
            # Persist to MongoDB
            try:
                d = report.get("data", {})
                verdict_map = {
                    'DEEPFAKE': 'AI-Generated',
                    'LIKELY FAKE': 'Suspicious',
                    'UNCERTAIN': 'Suspicious',
                    'LIKELY REAL': 'Authentic'
                }
                raw_verdict = d.get("verdict", "UNCERTAIN")
                verdict = verdict_map.get(raw_verdict, "Suspicious")
                
                await save_scan_internal(
                    email=user_email,
                    lab="video",
                    filename=filename,
                    verdict=verdict,
                    confidence=d.get("ai_probability", 0),
                    threat_level="critical" if verdict == "AI-Generated" else "high" if verdict == "Suspicious" else "low",
                    scan_id=f"vid-{uuid.uuid4().hex[:8]}",
                    extra={
                        "verdict_raw": raw_verdict,
                        "ai_probability": d.get("ai_probability", 0),
                        "agreement_count": d.get("agreement_count", 0)
                    }
                )
            except Exception as db_err:
                print(f"Failed to persist video scan to DB: {db_err}")

        except Exception as e:
            _jobs[job_id] = {"status": "error", "detail": str(e)}
        finally:
            # Clean up the temp file
            if os.path.exists(temp_path):
                os.remove(temp_path)

    # Note: Use asyncio.create_task for proper async execution in background
    asyncio.create_task(run_analysis())
    
    return {"status": "accepted", "job_id": job_id}

@router.get("/status/{job_id}")
async def get_video_status(job_id: str, user: dict = Depends(verify_paid_tier)):
    """
    Poll this endpoint for analysis result.
    """
    if job_id not in _jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    
    job = _jobs[job_id]
    if job.get("user_email") != user["email"]:
        raise HTTPException(status_code=403, detail="Not authorized to view this job status")
        
    return job
