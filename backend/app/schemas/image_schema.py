from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class ImageAnalysisRequest(BaseModel):
    image: str  # Base64 encoded image
    include_gradcam: bool = True

class RiskFactor(BaseModel):
    factor: str
    signal: str
    confidence: float

class ReassuringFactor(BaseModel):
    factor: str
    signal: str
    confidence: float

class ImageAnalysisResponse(BaseModel):
    risk_score: int
    fake_probability: float
    trust_score: float
    analysis_summary: str
    top_risk_factors: List[RiskFactor]
    reassuring_factors: List[ReassuringFactor]
    metadata_summary: str
    robustness_summary: str
    agreement: str
    agreement_note: Optional[str] = None
    agreement_count: Optional[str] = None
    reasons: Optional[List[str]] = None
    
    # Forensic details
    verdict: str
    threat_level: str
    confidence: float
    
    # Signals
    signals: Dict[str, float]
    signals_raw: Dict[str, float]
    
    # Robustness
    robustness: Dict[str, Any]
    
    # Metadata
    metadata_analysis: Dict[str, Any]
    
    # Explainability
    gradcam_heatmap: Optional[str] = None
    ela_image: Optional[str] = None
    weights_used: Dict[str, float]
    image_info: Dict[str, Any]
    processing_time: str
    engine_version: str
    benchmark_proof: Optional[Dict[str, Any]] = None
