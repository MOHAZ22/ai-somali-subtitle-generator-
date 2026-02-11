import numpy as np
import soundfile as sf
import os

# Create a simple test audio file with some audio
sample_rate = 16000
duration = 5  # seconds
t = np.linspace(0, duration, int(sample_rate * duration))
# Generate a simple tone (this won't transcribe meaningfully but tests the pipeline)
audio = np.sin(2 * np.pi * 440 * t) * 0.3  # 440Hz tone

# Save as WAV file
os.makedirs("test_audio", exist_ok=True)
sf.write("test_audio/test.wav", audio, sample_rate)
print("Test audio file created at test_audio/test.wav")
