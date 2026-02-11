from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TranscriptBase(BaseModel):
    media_file_id: int
    content: str
    language_code: str = "so"
    confidence_score: Optional[float] = None
    processing_time: Optional[float] = None

class TranscriptCreate(TranscriptBase):
    pass

class TranscriptUpdate(BaseModel):
    content: Optional[str] = None
    confidence_score: Optional[float] = None

class Transcript(TranscriptBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True
