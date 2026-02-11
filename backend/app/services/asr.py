import torch
import librosa
import numpy as np
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor
import os
from typing import List, Dict, Tuple
import logging

logger = logging.getLogger(__name__)

class SomaliASR:
    def __init__(self, model_name: str = None):
        """
        Initialize Somali ASR model
        For now, we'll use a multilingual model that supports Somali
        In production, you'd want to fine-tune on Somali data
        """
        self.model_name = model_name or " facebook/wav2vec2-large-xlsr-53"
        
        try:
            # Load pre-trained model and processor
            self.processor = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-large-xlsr-53")
            self.model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-large-xlsr-53")
            
            # Move model to GPU if available
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            self.model.to(self.device)
            self.model.eval()
            
            logger.info("ASR model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load ASR model: {e}")
            raise

    def preprocess_audio(self, audio_path: str) -> np.ndarray:
        """
        Preprocess audio file for ASR
        """
        try:
            # Load audio file
            audio, sr = librosa.load(audio_path, sr=16000)
            
            # Normalize audio
            audio = audio / np.max(np.abs(audio))
            
            return audio
        except Exception as e:
            logger.error(f"Error preprocessing audio: {e}")
            raise

    def transcribe(self, audio_path: str) -> Dict:
        """
        Transcribe audio file and return segments with timestamps
        """
        try:
            # Preprocess audio
            audio = self.preprocess_audio(audio_path)
            
            # Process audio
            input_values = self.processor(
                audio, 
                sampling_rate=16000, 
                return_tensors="pt", 
                padding="longest"
            ).input_values
            
            # Move to device
            input_values = input_values.to(self.device)
            
            # Get logits
            with torch.no_grad():
                logits = self.model(input_values).logits
            
            # Get predicted ids
            predicted_ids = torch.argmax(logits, dim=-1)
            
            # Decode predictions
            transcription = self.processor.batch_decode(predicted_ids)
            
            # For now, return simple transcription
            # In future, we'll add timestamp alignment
            result = {
                "text": transcription[0],
                "segments": self._create_segments(transcription[0], audio_path),
                "language": "so"  # Somali language code
            }
            
            return result
            
        except Exception as e:
            logger.error(f"Error during transcription: {e}")
            raise

    def _create_segments(self, text: str, audio_path: str) -> List[Dict]:
        """
        Create basic segments (will be enhanced later with proper alignment)
        """
        # Simple word splitting for demonstration
        words = text.split()
        segments = []
        
        if words:
            # Estimate duration from file (this is simplified)
            try:
                duration = librosa.get_duration(filename=audio_path)
                words_per_second = len(words) / duration if duration > 0 else 1
                
                start_time = 0
                for i, word in enumerate(words):
                    end_time = min(start_time + (1/words_per_second), duration)
                    segments.append({
                        "start": start_time,
                        "end": end_time,
                        "text": word,
                        "confidence": 0.9  # Placeholder confidence
                    })
                    start_time = end_time
            except:
                # Fallback if duration calculation fails
                segments = [{
                    "start": 0,
                    "end": 10,  # Default 10 seconds
                    "text": text,
                    "confidence": 0.9
                }]
        
        return segments

# Global instance
asr_model = None

def get_asr_model():
    """Get singleton ASR model instance"""
    global asr_model
    if asr_model is None:
        asr_model = SomaliASR()
    return asr_model
