import os
import uuid
import shutil
import tempfile
import asyncio
from fastapi import APIRouter, HTTPException, BackgroundTasks, UploadFile, File
# Pipeline import moved inside endpoint for lazy loading

router = APIRouter(prefix="/video", tags=["Video Forensics"])

# In-memory job store
_jobs = {}

@router.post("/analyze/async")
async def analyze_video_async(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...)
):
    """
    Async video analysis v10.0. Uploads file, starts background task, returns job_id.
    """
    job_id = "v10_" + str(uuid.uuid4())[:8]
    _jobs[job_id] = {"status": "processing", "result": None}

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
async def get_video_status(job_id: str):
    """
    Poll this endpoint for analysis result.
    """
    if job_id not in _jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    return _jobs[job_id]
