from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx
import json
import os
from typing import Optional
import asyncio

app = FastAPI(title="MoodDecode NLP API", description="Emotion analysis, crisis detection, and text summarization")

# Pydantic models for request/response
class TextInput(BaseModel):
    text: str

class MoodResponse(BaseModel):
    emotion: str
    confidence: float

class CrisisResponse(BaseModel):
    crisis_detected: bool
    severity: str
    confidence: float

class SummaryResponse(BaseModel):
    summary: str

# Groq API configuration
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "your-groq-api-key-here")
GROQ_BASE_URL = "https://api.groq.com/openai/v1/chat/completions"

async def call_groq_api(messages: list, temperature: float = 0.3, max_tokens: int = 150):
    """Make async call to Groq API"""
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "llama-3.1-70b-versatile",
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "response_format": {"type": "json_object"}
    }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(GROQ_BASE_URL, headers=headers, json=payload, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            raise HTTPException(status_code=500, detail=f"API call failed: {str(e)}")

@app.post("/analyze_mood", response_model=MoodResponse)
async def analyze_mood(input_data: TextInput):
    """Analyze the emotional tone of text"""
    
    mood_prompt = f"""
    You are an expert emotion analyst. Analyze the emotional tone of the given text and respond with valid JSON.

    Text to analyze: "{input_data.text}"

    Classify the emotion into one of these categories:
    - happy
    - sad
    - angry
    - fear
    - surprise
    - disgust
    - neutral

    Consider context, tone, and emotional intensity. Provide a confidence score (0.0-1.0).

    Examples:
    - "I'm thrilled about my promotion!" → happy (confidence: 0.9)
    - "This weather is okay I guess" → neutral (confidence: 0.7)
    - "I'm devastated by this news" → sad (confidence: 0.95)

    Respond with JSON format:
    {{
        "emotion": "emotion_name",
        "confidence": 0.0
    }}
    """

    messages = [
        {"role": "system", "content": "You are a professional emotion analysis API. Always respond with valid JSON."},
        {"role": "user", "content": mood_prompt}
    ]

    try:
        response = await call_groq_api(messages, temperature=0.2, max_tokens=100)
        content = response["choices"][0]["message"]["content"]
        result = json.loads(content)
        
        return MoodResponse(
            emotion=result["emotion"],
            confidence=result["confidence"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing mood: {str(e)}")

@app.post("/detect_crisis", response_model=CrisisResponse)
async def detect_crisis(input_data: TextInput):
    """Detect potential mental health crisis indicators"""
    
    crisis_prompt = f"""
    You are a mental health crisis detection system. Analyze the text for signs of mental health crisis, self-harm, or suicidal ideation.

    Text to analyze: "{input_data.text}"

    Crisis indicators include:
    - Suicidal thoughts or plans
    - Self-harm mentions
    - Feeling hopeless or trapped
    - Wanting to die or disappear
    - Feeling like a burden
    - Severe depression or despair
    - Substance abuse with harmful intent

    Severity levels:
    - "none": No crisis indicators
    - "low": Mild distress, general sadness
    - "moderate": Concerning language, needs attention
    - "high": Clear crisis indicators, immediate attention needed

    Examples:
    - "I'm having a bad day" → crisis_detected: false, severity: "low"
    - "I don't want to be here anymore" → crisis_detected: true, severity: "high"
    - "I'm feeling overwhelmed lately" → crisis_detected: false, severity: "moderate"

    Respond with JSON format:
    {{
        "crisis_detected": true/false,
        "severity": "severity_level",
        "confidence": 0.0
    }}
    """

    messages = [
        {"role": "system", "content": "You are a professional crisis detection API. Always respond with valid JSON. Err on the side of caution for safety."},
        {"role": "user", "content": crisis_prompt}
    ]

    try:
        response = await call_groq_api(messages, temperature=0.1, max_tokens=150)
        content = response["choices"][0]["message"]["content"]
        result = json.loads(content)
        
        return CrisisResponse(
            crisis_detected=result["crisis_detected"],
            severity=result["severity"],
            confidence=result["confidence"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error detecting crisis: {str(e)}")

@app.post("/summarize", response_model=SummaryResponse)
async def summarize_text(input_data: TextInput):
    """Summarize long text into a concise version"""
    
    summary_prompt = f"""
    You are a professional text summarization system. Create a concise, accurate summary of the given text.

    Text to summarize: "{input_data.text}"

    Guidelines:
    - Keep key information and main points
    - Maintain the original tone and context
    - Make it 20-30% of original length
    - Preserve important details
    - Use clear, readable language

    Examples:
    - Long article about climate change → Brief summary covering main points about causes, effects, and solutions
    - Personal story → Condensed version keeping emotional tone and key events
    - Technical document → Simplified version with main concepts

    Respond with JSON format:
    {{
        "summary": "your_concise_summary_here"
    }}
    """

    messages = [
        {"role": "system", "content": "You are a professional text summarization API. Always respond with valid JSON."},
        {"role": "user", "content": summary_prompt}
    ]

    try:
        response = await call_groq_api(messages, temperature=0.4, max_tokens=300)
        content = response["choices"][0]["message"]["content"]
        result = json.loads(content)
        
        return SummaryResponse(
            summary=result["summary"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error summarizing text: {str(e)}")

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