from pydantic import BaseModel

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