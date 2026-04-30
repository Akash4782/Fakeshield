from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.responses import Response
from app.schemas.text_schema import TextRequest
# Service import moved inside endpoints for lazy loading
import uuid

router = APIRouter(prefix="/api/v1/text", tags=["Text Detection"])

# In-memory async job store
_jobs: dict = {}
# In-memory scan store (fallback for PDF generation if DB is down)
_scans: dict = {}


@router.post("/analyze")
async def analyze_sync(req: TextRequest):
    """Sync — waits for full result. Use for direct testing."""
    from app.services.pipeline import run_text_pipeline
    try:
        result, _ = await run_text_pipeline(
            text=req.text,
            mode=req.mode,
            include_highlights=req.include_highlights,
        )
        return {"status": "success", "data": result}
    except ValueError as e:
        raise HTTPException(400, str(e))
    except Exception as e:
        raise HTTPException(500, str(e))


@router.post("/analyze/async")
async def analyze_async(
    req: TextRequest,
    background_tasks: BackgroundTasks
):
    """
    Async — returns job_id immediately.
    React polls /status/{job_id} every 2 seconds.
    This is the main endpoint your UI should use.
    """
    job_id = "job_" + str(uuid.uuid4())[:8]
    _jobs[job_id] = {"status": "processing", "data": None}

    async def run():
        from app.services.pipeline import run_text_pipeline
        try:
            result, _ = await run_text_pipeline(
                text=req.text,
                mode=req.mode,
                include_highlights=req.include_highlights,
            )
            _jobs[job_id] = {"status": "complete", "data": result}
            # Cache completed scan for PDF generation if DB is offline
            _scans[result["scan_id"]] = {"result": result, "text": req.text}
        except Exception as e:
            _jobs[job_id] = {"status": "error", "data": str(e)}

    background_tasks.add_task(run)
    return {"status": "accepted", "job_id": job_id}


@router.get("/status/{job_id}")
async def get_job_status(job_id: str):
    """React polls this every 2 seconds during analysis."""
    if job_id not in _jobs:
        raise HTTPException(404, "Job not found")
    return _jobs[job_id]


@router.post("/analyze/report")
async def analyze_with_report(req: TextRequest):
    """
    Returns JSON result + generates PDF report.
    Call this when user clicks 'Export Report'.
    """
    from app.services.pipeline import run_text_pipeline
    try:
        result, pdf_bytes = await run_text_pipeline(
            text=req.text,
            mode=req.mode,
            include_highlights=req.include_highlights,
            generate_report=True,
        )
        return {
            "status": "success",
            "data":   result,
        }
    except Exception as e:
        raise HTTPException(500, str(e))


@router.get("/report/{scan_id}")
async def download_report(scan_id: str):
    """Download PDF report for a completed scan."""
    from app.services.database   import get_scan_by_id
    from app.services.pdf_report import generate_pdf

    try:
        scan = await get_scan_by_id(scan_id)
        text = scan.get("text_preview", "") if scan else ""
    except Exception:
        scan = None
        text = ""

    if not scan:
        # Fallback to in-memory store if DB is down
        if scan_id in _scans:
            scan = _scans[scan_id]["result"]
            text = _scans[scan_id]["text"]
        else:
            raise HTTPException(404, "Scan not found (DB offline and memory cache missed)")

    pdf_bytes = generate_pdf(
        scan_id=scan_id,
        result=scan,
        text=text
    )
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition":
                f'attachment; filename="fakeshield_{scan_id}.pdf"'
        }
    )


@router.get("/history")
async def get_history(limit: int = 50):
    """Returns past scans from PostgreSQL."""
    from app.services.database import get_scan_history
    history = await get_scan_history(limit)
    return {"status": "success", "data": history}


@router.get("/health")
async def health():
    return {
        "status":  "online",
        "signals": "5 + Reasoning + ONNX + Binoculars",
        "mode":    "v16.5.0-RESEARCH-ELITE (Accelerated)",
        "version": "16.5.0-RESEARCH",
    }
