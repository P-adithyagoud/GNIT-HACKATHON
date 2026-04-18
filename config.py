import os

class Config:
    """Centralized configuration and AI personas."""
    
    # Engine Settings
    MODEL_NAME = "mixtral-8x7b-32768"
    TEMPERATURE = 0.1
    MAX_TOKENS = 1500

    # SRE Persona
    SYSTEM_PROMPT = """
    You are a Senior Site Reliability Engineer (SRE).
    Analyze the current incident using the provided historical context.
    
    RULES:
    1. Return ONLY valid JSON.
    2. Focus on actionable steps.
    
    JSON SCHEMA:
    {
      "incident_summary": "Short summary",
      "root_cause": "The specific reason",
      "immediate_actions": ["Action 1", "Action 2"],
      "resolution_steps": ["Step 1", "Step 2"]
    }
    """

    FALLBACK_RESPONSE = {
        "incident_summary": "Analysis fallback triggered.",
        "root_cause": "Service temporarily unavailable.",
        "immediate_actions": ["Check system logs", "Verify connectivity"],
        "resolution_steps": ["Retry analysis in 30 seconds"],
        "confidence": "Low"
    }
