"""
MongoDB integration proxy for text scans.
Replaces the old PostgreSQL system to use the unified MongoDB Atlas database.
"""
from app.database import text_results_collection
import json

async def save_scan(*args, **kwargs):
    # This was historically used to save to PostgreSQL.
    # It has been deprecated because text scans are now saved centrally
    # to MongoDB via `save_scan_internal` in dashboard_router.py.
    pass

async def get_scan_history(user_email: str, limit: int = 50) -> list:
    cursor = text_results_collection.find({"user_email": user_email}).sort("created_at", -1).limit(limit)
    docs = await cursor.to_list(length=limit)
    
    history = []
    for d in docs:
        res = d.get("full_result", {})
        
        # Format created_at to string if it's a datetime object
        created_at = d.get("created_at")
        if hasattr(created_at, "isoformat"):
            created_at = created_at.isoformat()
            
        history.append({
            "scan_id": d.get("scan_id"),
            "verdict": d.get("verdict"),
            "threat_level": d.get("threat_level"),
            "confidence": d.get("confidence") or res.get("confidence"),
            "word_count": res.get("word_count"),
            "text_preview": res.get("text_preview") or d.get("extra", {}).get("textPreview", ""),
            "created_at": created_at
        })
    return history

async def get_scan_by_id(scan_id: str) -> dict:
    doc = await text_results_collection.find_one({"scan_id": scan_id})
    if not doc:
        return {}
        
    res = doc.get("full_result", {})
    # For backward compatibility, ensure scan_id is in the top level of the returned dict
    if "scan_id" not in res:
        res["scan_id"] = scan_id
        
    return res
