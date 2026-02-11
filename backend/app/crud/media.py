from sqlalchemy.orm import Session
from app.models import MediaFile
from app.schemas.media import MediaFileCreate, MediaFileUpdate

def get_media_file(db: Session, media_file_id: int):
    return db.query(MediaFile).filter(MediaFile.id == media_file_id).first()

def get_user_media_files(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(MediaFile).filter(MediaFile.user_id == user_id).offset(skip).limit(limit).all()

def create_media_file(db: Session, media_file: MediaFileCreate, user_id: int):
    db_media_file = MediaFile(
        user_id=user_id,
        filename=media_file.filename,
        file_path="",  # Will be updated after upload
        file_size=media_file.file_size,
        mime_type=media_file.mime_type,
        status="uploaded"
    )
    db.add(db_media_file)
    db.commit()
    db.refresh(db_media_file)
    return db_media_file

def update_media_file(db: Session, media_file_id: int, media_file_update: MediaFileUpdate):
    db_media_file = db.query(MediaFile).filter(MediaFile.id == media_file_id).first()
    if db_media_file:
        for key, value in media_file_update.dict(exclude_unset=True).items():
            setattr(db_media_file, key, value)
        db.commit()
        db.refresh(db_media_file)
    return db_media_file

def delete_media_file(db: Session, media_file_id: int):
    db_media_file = db.query(MediaFile).filter(MediaFile.id == media_file_id).first()
    if db_media_file:
        db.delete(db_media_file)
        db.commit()
    return db_media_file
