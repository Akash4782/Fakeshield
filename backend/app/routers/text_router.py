from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.responses import Response
from app.schemas.text_schema import TextRequest
from app.dependencies import get_current_user, verify_paid_tier
from app.routers.dashboard_router import save_scan_internal
from fastapi import Depends
# Service import moved inside endpoints for lazy loading
import uuid

router = APIRouter(prefix="/api/v1/text", tags=["Text Detection"])

# In-memory async job store
_jobs: dict = {}
# In-memory scan store (fallback for PDF generation if DB is down)
_scans: dict = {}


@router.post("/analyze")
async def analyze_sync(req: TextRequest, user: dict = Depends(get_current_user)):
    """Sync — waits for full result. Use for direct testing."""
    from app.services.pipeline import run_text_pipeline
    try:
        result, _ = await run_text_pipeline(
            user_email=user["email"],
            text=req.text,
            mode=req.mode,
            include_highlights=req.include_highlights,
        )
        
        # Persist to MongoDB
        try:
            await save_scan_internal(
                email=user["email"],
                lab="text",
                filename=f"text_scan_{result['scan_id'][:6]}.txt",
                verdict=result.get("verdict", "Suspicious"),
                confidence=result.get("score", 0),
                threat_level=result.get("threat_level", "low").lower(),
                scan_id=result.get("scan_id", f"txt-{uuid.uuid4().hex[:8]}"),
                extra={
                    "mode": req.mode,
                    "confidence_level": result.get("confidence_level")
                },
                full_result=result
            )
        except Exception as db_err:
            print(f"Failed to persist text scan to DB: {db_err}")

        return {"status": "success", "data": result}
    except ValueError as e:
        raise HTTPException(400, str(e))
    except Exception as e:
        raise HTTPException(500, str(e))


@router.post("/analyze/async")
async def analyze_async(
    req: TextRequest,
    background_tasks: BackgroundTasks,
    user: dict = Depends(get_current_user)
):
    """
    Async — returns job_id immediately.
    React polls /status/{job_id} every 2 seconds.
    This is the main endpoint your UI should use.
    """
    job_id = "job_" + str(uuid.uuid4())[:8]
    _jobs[job_id] = {"status": "processing", "data": None, "user_email": user["email"]}

    async def run():
        from app.services.pipeline import run_text_pipeline
        try:
            result, _ = await run_text_pipeline(
                user_email=user["email"],
                text=req.text,
                mode=req.mode,
                include_highlights=req.include_highlights,
            )
            _jobs[job_id] = {"status": "complete", "data": result, "user_email": user["email"]}
            # Cache completed scan for PDF generation if DB is offline
            _scans[result["scan_id"]] = {"result": result, "text": req.text, "user_email": user["email"]}
            
            # Persist to MongoDB
            try:
                await save_scan_internal(
                    email=user["email"],
                    lab="text",
                    filename=f"text_scan_{result['scan_id'][:6]}.txt",
                    verdict=result.get("verdict", "Suspicious"),
                    confidence=result.get("score", 0),
                    threat_level=result.get("threat_level", "low").lower(),
                    scan_id=result.get("scan_id", f"txt-{uuid.uuid4().hex[:8]}"),
                    extra={
                        "mode": req.mode,
                        "confidence_level": result.get("confidence_level")
                    },
                    full_result=result
                )
            except Exception as db_err:
                print(f"Failed to persist text scan to DB: {db_err}")

        except Exception as e:
            _jobs[job_id] = {"status": "error", "data": str(e), "user_email": user["email"]}

    background_tasks.add_task(run)
    return {"status": "accepted", "job_id": job_id}


@router.get("/status/{job_id}")
async def get_job_status(job_id: str, user: dict = Depends(get_current_user)):
    """React polls this every 2 seconds during analysis."""
    if job_id not in _jobs:
        raise HTTPException(404, "Job not found")
    
    job = _jobs[job_id]
    if job.get("user_email") != user["email"]:
        raise HTTPException(403, "Not authorized to view this job status")
        
    return job


@router.post("/analyze/report")
async def analyze_with_report(req: TextRequest, user: dict = Depends(get_current_user)):
    """
    Returns JSON result + generates PDF report.
    Call this when user clicks 'Export Report'.
    """
    from app.services.pipeline import run_text_pipeline
    try:
        result, pdf_bytes = await run_text_pipeline(
            user_email=user["email"],
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
@router.get("/report/{scan_id}.pdf")
async def download_report(scan_id: str, user: dict = Depends(get_current_user)):
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
            scan_owner = _scans[scan_id].get("user_email")
        else:
            raise HTTPException(404, "Scan not found (DB offline and memory cache missed)")
    else:
        scan_owner = scan.get("user_email")

    if scan_owner and scan_owner != user["email"]:
        raise HTTPException(403, "Not authorized to download this report")

    try:
        pdf_bytes = generate_pdf(
            scan_id=scan_id,
            result=scan,
            text=text
        )
    except Exception as e:
        print(f"PDF GENERATION ERROR: {e}")
        raise HTTPException(500, f"Internal PDF Engine Error: {str(e)}")

    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="FakeShield_Report_{scan_id[:8]}.pdf"',
            "Access-Control-Expose-Headers": "Content-Disposition"
        }
    )


@router.get("/scan/{scan_id}")
async def get_scan_details(scan_id: str, user: dict = Depends(get_current_user)):
    """Fetch full forensic scan details for the UI."""
    from app.services.database import get_scan_by_id
    
    try:
        scan = await get_scan_by_id(scan_id)
    except Exception as e:
        print(f"Failed to fetch scan from DB: {e}")
        scan = None

    if not scan:
        if scan_id in _scans:
            scan = _scans[scan_id]["result"]
        else:
            raise HTTPException(404, "Scan not found")

    if scan.get("user_email") and scan.get("user_email") != user["email"]:
        raise HTTPException(403, "Not authorized to view this scan")

    # Ensure signals and other JSON fields are parsed if they came from Postgres as strings/objects
    return {"status": "success", "data": scan}


@router.get("/history")
async def get_history(limit: int = 50, user: dict = Depends(get_current_user)):
    """Returns past scans from PostgreSQL."""
    from app.services.database import get_scan_history
    history = await get_scan_history(user["email"], limit)
    return {"status": "success", "data": history}


@router.get("/health")
async def health():
    return {
        "status": "healthy",
        "engine": "Vanguard",
        "version": "v85.26-SOVEREIGN",
        "active_models": ["DeBERTa-v3-L", "Binoculars-Sovereign", "Roberta-Large", "MiniLM-Semantic"]
    }
