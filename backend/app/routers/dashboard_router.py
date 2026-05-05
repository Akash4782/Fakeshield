"""
dashboard_router.py
Provides endpoints to save and retrieve per-user scan history across all labs.
"""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional, Any, Dict
from datetime import datetime, timezone
from bson import ObjectId
from app.dependencies import get_current_user
from app.database import (
    text_results_collection,
    image_results_collection,
    audio_results_collection,
    video_results_collection,
)

router = APIRouter(prefix="/api/v1/dashboard", tags=["Dashboard"])


# ──────────────────────────────────────────────
# Schema for saving a scan result
# ──────────────────────────────────────────────
class ScanRecord(BaseModel):
    lab: str            # "text" | "image" | "audio" | "video"
    filename: str
    verdict: str        # "AI-Generated" | "Authentic" | "Suspicious"
    confidence: float   # 0.0 – 1.0
    threat_level: str   # "critical" | "high" | "medium" | "low" | "safe"
    scan_id: str
    extra: Optional[Dict[str, Any]] = None  # lab-specific extras


def _collection_for(lab: str):
    mapping = {
        "text":  text_results_collection,
        "image": image_results_collection,
        "audio": audio_results_collection,
        "video": video_results_collection,
    }
    col = mapping.get(lab)
    if col is None:
        raise HTTPException(400, f"Unknown lab: {lab}")
    return col


def _serialize(doc: dict) -> dict:
    """Make MongoDB document JSON-serializable."""
    doc["_id"] = str(doc["_id"])
    if isinstance(doc.get("created_at"), datetime):
        doc["created_at"] = doc["created_at"].isoformat()
    return doc


async def save_scan_internal(
    email: str,
    lab: str,
    filename: str,
    verdict: str,
    confidence: float,
    threat_level: str,
    scan_id: str,
    extra: dict = None,
    full_result: dict = None,
):
    """
    Unified persistence helper — saves any scan result to the respective MongoDB collection.
    Automatically segments by user_email for isolation.
    """
    try:
        col = _collection_for(lab)
    except HTTPException:
        print(f"[DB] Invalid lab: {lab}")
        return

    doc = {
        "user_email": email,
        "lab":        lab,
        "filename":   filename,
        "verdict":    verdict,
        "confidence": confidence,
        "threat_level": threat_level,
        "scan_id":    scan_id,
        "extra":      extra or {},
        "full_result": full_result or {},
        "created_at": datetime.now(timezone.utc),
    }

    try:
        await col.insert_one(doc)
        print(f"[DB] {lab.capitalize()} scan {scan_id} saved for {email}")
    except Exception as e:
        print(f"[DB] Failed to save {lab} scan: {e}")


# ──────────────────────────────────────────────
# POST /api/v1/dashboard/save  — called by each lab after a scan
# ──────────────────────────────────────────────
@router.post("/save")
async def save_scan(record: ScanRecord, user: dict = Depends(get_current_user)):
    await save_scan_internal(
        email=user["email"],
        lab=record.lab,
        filename=record.filename,
        verdict=record.verdict,
        confidence=record.confidence,
        threat_level=record.threat_level,
        scan_id=record.scan_id,
        extra=record.extra
    )
    return {"status": "saved", "scan_id": record.scan_id}


# ──────────────────────────────────────────────
# GET /api/v1/dashboard/history  — recent scans for this user
# ──────────────────────────────────────────────
@router.get("/history")
async def get_history(limit: int = 20, user: dict = Depends(get_current_user)):
    email = user["email"]
    query = {"user_email": email}

    # Fetch from all four collections concurrently
    import asyncio
    async def _fetch(col, lab):
        cursor = col.find(query, {"extra": 0}).sort("created_at", -1).limit(limit)
        docs = await cursor.to_list(length=limit)
        for d in docs:
            d["lab"] = lab   # ensure lab field always present
        return docs

    results = await asyncio.gather(
        _fetch(text_results_collection,  "text"),
        _fetch(image_results_collection, "image"),
        _fetch(audio_results_collection, "audio"),
        _fetch(video_results_collection, "video"),
    )

    # Merge, sort by time, take latest `limit` overall
    all_scans = []
    for batch in results:
        for doc in batch:
            all_scans.append(_serialize(doc))

    all_scans.sort(key=lambda x: x.get("created_at", ""), reverse=True)
    return {"scans": all_scans[:limit]}


# ──────────────────────────────────────────────
# GET /api/v1/dashboard/stats  — aggregate stats for this user
# ──────────────────────────────────────────────
@router.get("/stats")
async def get_stats(user: dict = Depends(get_current_user)):
    email = user["email"]
    query = {"user_email": email}

    async def _count_verdicts(col, regex_pattern):
        return await col.count_documents({**query, "verdict": {"$regex": regex_pattern, "$options": "i"}})

    import asyncio
    collections = [
        text_results_collection,
        image_results_collection,
        audio_results_collection,
        video_results_collection,
    ]
    lab_names = ["text", "image", "audio", "video"]

    # Regex patterns for different versions of the labs
    AI_PATTERN = "AI-Generated|AI GENERATED|DEEPFAKE|LIKELY_AI|LIKELY FAKE|AI"
    AUTHENTIC_PATTERN = "Authentic|AUTHENTIC|LIKELY HUMAN|LIKELY_HUMAN|LIKELY REAL|HUMAN"
    SUSPICIOUS_PATTERN = "Suspicious|UNCERTAIN|REJECTED"

    counts = await asyncio.gather(*[col.count_documents(query) for col in collections])
    total  = sum(counts)

    ai_counts        = await asyncio.gather(*[_count_verdicts(c, AI_PATTERN) for c in collections])
    authentic_counts = await asyncio.gather(*[_count_verdicts(c, AUTHENTIC_PATTERN) for c in collections])
    suspicious_counts = await asyncio.gather(*[_count_verdicts(c, SUSPICIOUS_PATTERN) for c in collections])

    total_ai        = sum(ai_counts)
    total_authentic = sum(authentic_counts)
    total_suspicious = sum(suspicious_counts)
    total_threats   = total_ai + total_suspicious

    print(f"[DEBUG-STATS] User: {email}")
    print(f"[DEBUG-STATS] Counts: {counts}")
    print(f"[DEBUG-STATS] AI: {ai_counts} -> Total: {total_ai}")
    print(f"[DEBUG-STATS] Authentic: {authentic_counts} -> Total: {total_authentic}")
    print(f"[DEBUG-STATS] Suspicious: {suspicious_counts} -> Total: {total_suspicious}")

    return {
        "total_scans": total,
        "total_threats": total_threats,
        "total_authentic": total_authentic,
        "ai_detected": total_ai,
        "lab_breakdown": {
            lab: {"total": counts[i], "ai": ai_counts[i]}
            for i, lab in enumerate(lab_names)
        },
    }


# ──────────────────────────────────────────────
# GET /api/v1/dashboard/scan/{scan_id} — fetch details for ANY scan
# ──────────────────────────────────────────────
@router.get("/scan/{scan_id}")
async def get_scan_details(scan_id: str, user: dict = Depends(get_current_user)):
    email = user["email"]
    
    # Check all 4 collections
    collections = [
        ("text",  text_results_collection),
        ("image", image_results_collection),
        ("audio", audio_results_collection),
        ("video", video_results_collection),
    ]
    
    for lab, col in collections:
        doc = await col.find_one({"scan_id": scan_id, "user_email": email})
        if doc:
            return {"status": "success", "lab": lab, "data": _serialize(doc)}
            
    raise HTTPException(404, "Scan not found or not authorized")
