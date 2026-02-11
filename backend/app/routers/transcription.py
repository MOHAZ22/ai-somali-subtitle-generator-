from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.routers.auth import get_current_active_user
from app.models import User
from app.services.transcription import transcription_service
from app.crud import media as media_crud
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/transcribe", tags=["transcription"])

@router.post("/{media_id}")
async def transcribe_media(
    media_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Transcribe a media file
    """
    try:
        # Verify media file exists and belongs to user
        media_file = media_crud.get_media_file(db, media_id)
        if not media_file:
            raise HTTPException(status_code=404, detail="Media file not found")
        
        if media_file.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not authorized to transcribe this file")
        
        # Perform transcription
        result = transcription_service.transcribe_media(db, media_id, current_user.id)
        
        return {
            "success": True,
            "message": "Transcription completed successfully",
            "data": result
        }
        
    except Exception as e:
        logger.error(f"Transcription error: {e}")
        raise HTTPException(status_code=500, detail=f"Transcription failed: {str(e)}")

@router.get("/{media_id}")
async def get_transcription(
    media_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get transcription results for a media file
    """
    from app.crud import transcript as transcript_crud
    
    # Verify media file exists and belongs to user
    media_file = media_crud.get_media_file(db, media_id)
    if not media_file:
        raise HTTPException(status_code=404, detail="Media file not found")
    
    if media_file.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this transcription")
    
    # Get transcript
    transcript = transcript_crud.get_transcript_by_media_file(db, media_id)
    if not transcript:
        raise HTTPException(status_code=404, detail="Transcription not found")
    
    return {
        "success": True,
        "data": transcript
    }
