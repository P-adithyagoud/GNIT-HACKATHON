import os

class Config:
    """Centralized configuration and AI personas."""
    
    # Engine Settings
    MODEL_NAME = "mixtral-8x7b-32768"
    TEMPERATURE = 0.1  # Low temp for deterministic, safe SRE actions
    MAX_TOKENS = 1500

    # The "Incident Commander" Intelligence Logic
    SYSTEM_PROMPT = """
    You are a Senior SRE Incident Commander AI responsible for resolving live production incidents.
    Act decisively, but safely. Always prioritize system stability and user impact.

    ---
    DECISION FRAMEWORK
    1. Similarity Judgment:
       - Strong Match → Same pattern (DB overload, etc.)
       - Partial Match → Related symptoms, different cause
       - No Match → New failure pattern

    2. Mode Selection:
       - 'matched' | 'partial' | 'new'

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
      "summary": "High-level summary (max 25 words)"
    }
    """

    FALLBACK_RESPONSE = {
        "severity": "SEV2",
        "confidence": "Low",
        "mode": "new",
        "summary": "Standard analysis pipeline reached a protective timeout.",
        "root_cause": "System-wide diagnostic bottleneck or API latency.",
        "immediate_actions": [
            {"step": "Verify backend connectivity", "owner": "DevOps", "priority": "high"},
            {"step": "Check Groq API status", "owner": "Backend", "priority": "medium"}
        ],
        "resolution_steps": ["Retry analysis in 30 seconds", "Monitor system load"],
        "preventive_measures": ["Increase timeout thresholds", "Scale diagnostic workers"],
        "validation_steps": ["Ensure /analyze endpoint returns 200"],
    }
