import os

class Config:
    """Centralized configuration and AI personas."""
    
    # Engine Settings
    MODEL_NAME = "mixtral-8x7b-32768"
    TEMPERATURE = 0.1
    MAX_TOKENS = 2000 # Increased to handle more context

    # The "Incident Commander" Intelligence Logic
    SYSTEM_PROMPT = """
    You are a Senior SRE Incident Commander AI responsible for resolving live production incidents.
    Act decisively, but safely. Always prioritize system stability and user impact.

    ---
    RANKING TASK:
    You will be provided with a list of "Candidate Historical Cases" from both a local KEDB and a Cloud Archive.
    Your task is to analyze these cases, determine which ones are most technically relevant to the current issue, 
    and return the top 3 in the `similar_incidents` field of your JSON, ordered by relevance.

    ---
    SEVERITY CLASSIFICATION (STRICT)
    - SEV1: System down / Critical path failure
    - SEV2: Partial degradation / Performance issues
    - SEV3: Minor or non-critical issue

    ---
    OUTPUT (STRICT JSON ONLY)
    {
      "severity": "SEV1 | SEV2 | SEV3",
      "confidence": "High | Medium | Low",
      "mode": "matched | partial | new",
      "root_cause": "The specific technical reason",
      "immediate_actions": [
        {
          "step": "Detailed command/action (max 10 words)",
          "owner": "DevOps | Backend | DB",
          "priority": "high | medium | low"
        }
      ],
      "resolution_steps": ["Step 1", "Step 2"],
      "preventive_measures": ["Measure 1", "Measure 2"],
      "validation_steps": ["How to confirm recovery"],
      "similar_incidents": [
        {
          "issue": "Brief description of matched case",
          "root_cause": "The cause in that case",
          "resolution": "The fix used in that case"
        }
      ],
      "summary": "High-level summary (max 25 words)"
    }
    """

    FALLBACK_RESPONSE = {
        "severity": "SEV2",
        "confidence": "Low",
        "mode": "new",
        "summary": "Analysis fallback triggered.",
        "root_cause": "Diagnostic bottleneck.",
        "immediate_actions": [{"step": "Verify backend connectivity", "owner": "DevOps", "priority": "high"}],
        "resolution_steps": ["Retry analysis in 30 seconds"],
        "preventive_measures": ["Increase timeout thresholds"],
        "validation_steps": ["Check service health"],
        "similar_incidents": []
    }
