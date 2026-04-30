from pydantic import BaseModel, Field
from typing import Optional, List

class TextRequest(BaseModel):
    text: str = Field(
        ...,
        min_length=20,
        max_length=15000,
        description="Text to analyse for AI detection"
    )
    include_highlights: bool = Field(
        default=True,
        description="Include sentence-level highlighting"
    )
    mode: str = Field(
        default="deep",
        description="'fast' = RoBERTa only, 'deep' = all 5 signals"
    )

class SignalScores(BaseModel):
    deberta:        float
    embedding:      float
    gpt2_entropy:   float
    stylometric:    float

class StylometricDetails(BaseModel):
    burstiness_cv:      float
    ai_phrases:         int
    ttr:                float
    passives:           int
    repeat_starter:     int

class SentenceHighlight(BaseModel):
    sentence:  str
    ai_score:  Optional[float]
    label:     str           # AI | LIKELY_AI | UNCERTAIN | HUMAN | too_short

class LinguisticProfile(BaseModel):
    syntactic_complexity: str   # LOW | MODERATE | HIGH
    lexical_diversity:    str
    pacing_consistency:   str
    entropy_bits_per_char: float
    burstiness_raw:        float

class TextResult(BaseModel):
    verdict:              str
    threat_level:         str  # LOW | MODERATE | HIGH | CRITICAL
    confidence:           float
    confidence_level:     str  # LOW | MEDIUM | HIGH
    agreement_score:      int  # 0-4
    stability_score:      float
    signals:              SignalScores
    linguistic_profile:   LinguisticProfile
    sentence_highlights:  List[SentenceHighlight]
    indicators:           List[str]
    stylometric_details:  Optional[StylometricDetails] = None
    word_count:           int
    char_count:           int
    sentence_count:       int
    processing_time:      str
    processing_mode:      str
    engine_version:       str

class TextResponse(BaseModel):
    status: str
    data:   TextResult
