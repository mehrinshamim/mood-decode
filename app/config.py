from dotenv import load_dotenv
import os

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "your-groq-api-key-here")
GROQ_BASE_URL = "https://api.groq.com/openai/v1/chat/completions" 