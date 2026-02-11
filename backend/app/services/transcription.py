from sqlalchemy.orm import Session
from app.services.asr import get_asr_model
from app.crud import media as media_crud, transcript as transcript_crud
from app.schemas.transcript import TranscriptCreate
from app.models import MediaFile
import logging
import time

logger = logging.getLogger(__name__)

class TranscriptionService:
    def __init__(self):
        # Don't load ASR model immediately - load it when needed
        self.asr_model = None

    def _get_asr_model(self):
        """Lazy load ASR model when needed"""
        if self.asr_model is None:
            from app.services.asr import get_asr_model
            self.asr_model = get_asr_model()
        return self.asr_model

    def transcribe_media(self, db: Session, media_file_id: int, user_id: int) -> dict:
        """
        Transcribe a media file and save results to database
        """
        try:
            # Get media file
            media_file = media_crud.get_media_file(db, media_file_id)
            if not media_file:
                raise ValueError("Media file not found")
            
            # Check ownership
            if media_file.user_id != user_id:
                raise ValueError("Not authorized to transcribe this file")
            
            # Update status to processing
            media_crud.update_media_file(db, media_file_id, {"status": "processing"})
            
            # Start transcription
            start_time = time.time()
            asr_model = self._get_asr_model()
            result = asr_model.transcribe(media_file.file_path)
            processing_time = time.time() - start_time
            
            # Save transcription to database
            transcript_data = TranscriptCreate(
                media_file_id=media_file_id,
                content=result["text"],
                language_code=result["language"],
                confidence_score=self._calculate_average_confidence(result["segments"]),
                processing_time=processing_time
            )
            
            transcript = transcript_crud.create_transcript(db, transcript_data)
            
            # Update media file status
            media_crud.update_media_file(db, media_file_id, {"status": "completed"})
            
            return {
                "transcript_id": transcript.id,
                "segments": result["segments"],
                "processing_time": processing_time,
                "success": True
            }
            
        except Exception as e:
            logger.error(f"Transcription failed: {e}")
            # Update status to failed
            try:
                media_crud.update_media_file(db, media_file_id, {"status": "failed"})
            except:
                pass
            raise

    def _calculate_average_confidence(self, segments: list) -> float:
        """Calculate average confidence from segments"""
        if not segments:
            return 0.0
        confidences = [seg.get("confidence", 0) for seg in segments]
        return sum(confidences) / len(confidences) if confidences else 0.0

# Singleton instance
transcription_service = TranscriptionService()
