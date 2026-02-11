import os
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
import uuid
from app.db.database import get_db
from app.crud import media as media_crud
from app.crud import user as user_crud
from app.schemas.media import MediaFileCreate, MediaFileUpdate
from app.routers.auth import get_current_active_user
from app.models import User

router = APIRouter(prefix="/media", tags=["media"])

# Create uploads directory
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Allowed file types
ALLOWED_EXTENSIONS = {
    'audio': ['.mp3', '.wav', '.flac', '.m4a'],
    'video': ['.mp4', '.mkv', '.avi', '.mov', '.webm']
}

MAX_FILE_SIZE = 500 * 1024 * 1024  # 500MB

@router.post("/upload")
async def upload_media(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    # Validate file size
    contents = await file.read()
    file_size = len(contents)
    if file_size > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File too large. Maximum size is 500MB.")
    
    # Reset file pointer
    await file.seek(0)
    
    # Validate file extension
    file_ext = os.path.splitext(file.filename)[1].lower()
    is_valid_audio = file_ext in ALLOWED_EXTENSIONS['audio']
    is_valid_video = file_ext in ALLOWED_EXTENSIONS['video']
    
    if not (is_valid_audio or is_valid_video):
        raise HTTPException(status_code=400, detail="Invalid file type. Supported formats: MP3, WAV, FLAC, M4A, MP4, MKV, AVI, MOV, WEBM")
    
    # Generate unique filename
    unique_filename = f"{uuid.uuid4()}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)
    
    # Save file
    with open(file_path, "wb") as buffer:
        buffer.write(contents)
    
    # Create media file record
    media_file_create = MediaFileCreate(
        filename=file.filename,
        file_size=file_size,
        mime_type=file.content_type
    )
    
    db_media_file = media_crud.create_media_file(
        db=db, 
        media_file=media_file_create, 
        user_id=current_user.id
    )
    
    # Update file path in database
    media_update = MediaFileUpdate(file_path=file_path)
    media_crud.update_media_file(db, db_media_file.id, media_update)
    
    return {
        "id": db_media_file.id,
        "filename": file.filename,
        "file_size": file_size,
        "status": "uploaded",
        "message": "File uploaded successfully"
    }

@router.get("/history")
async def get_user_media_history(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    media_files = media_crud.get_user_media_files(db, current_user.id, skip, limit)
    return media_files

@router.get("/{media_id}")
async def get_media_info(
    media_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    media_file = media_crud.get_media_file(db, media_id)
    if not media_file:
        raise HTTPException(status_code=404, detail="Media file not found")
    
    # Check if user owns this file
    if media_file.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this file")
    
    return media_file

@router.get("/{media_id}/download")
async def download_media(
    media_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    media_file = media_crud.get_media_file(db, media_id)
    if not media_file:
        raise HTTPException(status_code=404, detail="Media file not found")
    
    # Check if user owns this file
    if media_file.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this file")
    
    if not os.path.exists(media_file.file_path):
        raise HTTPException(status_code=404, detail="File not found on server")
    
    return FileResponse(
        path=media_file.file_path,
        filename=media_file.filename,
        media_type=media_file.mime_type
    )

@router.delete("/{media_id}")
async def delete_media(
    media_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    media_file = media_crud.get_media_file(db, media_id)
    if not media_file:
        raise HTTPException(status_code=404, detail="Media file not found")
    
    # Check if user owns this file
    if media_file.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this file")
    
    # Delete file from filesystem
    if os.path.exists(media_file.file_path):
        os.remove(media_file.file_path)
    
    # Delete from database
    media_crud.delete_media_file(db, media_id)
    
    return {"message": "Media file deleted successfully"}
