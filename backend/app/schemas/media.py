from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class MediaFileBase(BaseModel):
    filename: str
    mime_type: str
    file_size: int

class MediaFileCreate(MediaFileBase):
    pass

class MediaFileUpdate(BaseModel):
    status: Optional[str] = None
    duration: Optional[float] = None

class MediaFile(MediaFileBase):
    id: int
    user_id: int
    file_path: str
    status: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class MediaFileResponse(MediaFile):
    pass
