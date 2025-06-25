import logging
from logging.handlers import RotatingFileHandler
import os
from fastapi import FastAPI
from app.routes.nlp import router as nlp_router

# Logging setup
log_dir = os.path.join(os.path.dirname(__file__), 'logs')
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, 'error.log')

logger = logging.getLogger()
logger.setLevel(logging.INFO)

file_handler = RotatingFileHandler(log_file, maxBytes=1024*1024, backupCount=3)
file_handler.setLevel(logging.ERROR)
file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(file_formatter)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_formatter = logging.Formatter('%(levelname)s - %(message)s')
console_handler.setFormatter(console_formatter)

if not logger.hasHandlers():
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
else:
    logger.handlers.clear()
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

app = FastAPI(title="MoodDecode NLP API", description="Emotion analysis, crisis detection, and text summarization")

app.include_router(nlp_router)

@app.get("/")
async def root():
    """API health check and info"""
    return {
        "message": "MoodDecode NLP API is running!",
        "endpoints": {
            "mood_analysis": "/analyze_mood",
            "crisis_detection": "/detect_crisis", 
            "text_summarization": "/summarize"
        },
        "status": "healthy"
    }

@app.get("/health")
async def health_check():
    """Simple health check endpoint"""
    return {"status": "healthy", "api": "MoodDecode NLP API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)