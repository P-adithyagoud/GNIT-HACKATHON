import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GROQ_API_KEY = os.getenv('GROQ_API_KEY')
    GROQ_API_URL = 'https://api.groq.com/openai/v1/chat/completions'
    
    # Supabase configuration
    SUPABASE_URL = os.getenv('SUPABASE_URL')
    SUPABASE_KEY = os.getenv('SUPABASE_KEY')

    # Model configuration
    MODEL_NAME = 'mixtral-8x7b-32768'
    TEMPERATURE = 0.1
    MAX_TOKENS = 1000

    SYSTEM_PROMPT = """You are a senior DevOps and Site Reliability Engineer.
Your goal is to provide a structured, actionable response to a production incident.
Use the provided similar past incidents as context to inform your analysis.

STRICT RULES:
1. Return ONLY valid JSON.
2. NO markdown formatting, NO extra text.
3. Actions must be specific and executable.
4. If similar incidents are provided, leverage their root causes and resolutions.

STRICT JSON FORMAT:
{
  "incident_summary": "Short 1-sentence summary",
  "root_cause": "Specific technical root cause based on context",
  "immediate_actions": ["Action 1", "Action 2", "Action 3"],
  "resolution_steps": ["Step 1", "Step 2"],
  "confidence": "High | Medium | Low",
  "similar_incidents": []
}"""

    FALLBACK_RESPONSE = {
        "incident_summary": "Analysis failed due to system error.",
        "root_cause": "Internal processing error or API timeout.",
        "immediate_actions": ["Check system logs", "Notify on-call engineer"],
        "resolution_steps": ["Retry analysis later"],
        "confidence": "Low",
        "similar_incidents": []
    }
