from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, media, transcription
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="AI-Powered Somali Subtitle Generator",
    description="Automatic speech recognition and subtitle generation for Somali language",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(media.router)
app.include_router(transcription.router)

@app.get("/")
async def root():
    return {"message": "AI-Powered Somali Subtitle Generator API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)