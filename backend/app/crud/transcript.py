from sqlalchemy.orm import Session
from app.models import Transcript
from app.schemas.transcript import TranscriptCreate, TranscriptUpdate

def get_transcript(db: Session, transcript_id: int):
    return db.query(Transcript).filter(Transcript.id == transcript_id).first()

def get_transcript_by_media_file(db: Session, media_file_id: int):
    return db.query(Transcript).filter(Transcript.media_file_id == media_file_id).first()

def create_transcript(db: Session, transcript: TranscriptCreate):
    db_transcript = Transcript(**transcript.dict())
    db.add(db_transcript)
    db.commit()
    db.refresh(db_transcript)
    return db_transcript

def update_transcript(db: Session, transcript_id: int, transcript_update: TranscriptUpdate):
    db_transcript = db.query(Transcript).filter(Transcript.id == transcript_id).first()
    if db_transcript:
        for key, value in transcript_update.dict(exclude_unset=True).items():
            setattr(db_transcript, key, value)
        db.commit()
        db.refresh(db_transcript)
    return db_transcript

def delete_transcript(db: Session, transcript_id: int):
    db_transcript = db.query(Transcript).filter(Transcript.id == transcript_id).first()
    if db_transcript:
        db.delete(db_transcript)
        db.commit()
    return db_transcript
