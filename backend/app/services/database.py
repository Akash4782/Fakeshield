"""
MongoDB integration wrapper for text forensics.
Redirects old PostgreSQL calls to the new unified MongoDB dashboard.
"""
import asyncio
from app.routers.dashboard_router import save_scan_internal

async def save_scan(
    user_email: str,
    scan_id: str,
    verdict: str,
    threat_level: str,
    confidence: float,
    confidence_level: str,
    agreement_score: int,
    stability_score: float,
    signals: dict,
    linguistic_profile: dict,
    stylometric_details: dict,
    word_count: int,
    processing_time: str,
    text_preview: str,
):
    """
    Adapter that maps the old PostgreSQL-style call to the new MongoDB unified dashboard.
    """
    extra = {
        "confidence_level": confidence_level,
        "agreement_score": agreement_score,
        "stability_score": stability_score,
        "signals": signals,
        "linguistic_profile": linguistic_profile,
        "stylometric_details": stylometric_details,
        "word_count": word_count,
        "processing_time": processing_time,
        "text_preview": text_preview
    }
    
    # Save using the unified MongoDB logic
    await save_scan_internal(
        email=user_email,
        lab="text",
        filename="Text Analysis",
        verdict=verdict,
        confidence=confidence,
        threat_level=threat_level,
        scan_id=scan_id,
        extra=extra,
        full_result=extra # Save the same data as full result for now
    )

async def get_scan_history(user_email: str, limit: int = 50) -> list:
    """Mock for old history calls — frontend now uses dashboard_router.get_history directly."""
    return []

async def get_scan_by_id(scan_id: str) -> dict:
    """Mock for old scan details calls — frontend now uses dashboard_router.get_scan_details directly."""
    return {}
