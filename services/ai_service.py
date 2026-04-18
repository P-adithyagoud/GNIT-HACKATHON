import os
import httpx
from config import Config

class AIService:
    """
    SRE Expert Engine: Conducts intelligent analysis using Groq infrastructure.
    Enhanced to prioritize Known Error Database (KEDB) context.
    """

    @staticmethod
    def generate_resolution_analysis(query, matched_knowledge):
        """Generates a detailed incident report using Hybrid KEDB context."""
        client_key = os.getenv("GROQ_API_KEY")
        if not client_key:
            return None

        # Build context from Known Error Database (KEDB) entries
        knowledge_context = ""
        for i, inc in enumerate(matched_knowledge):
            knowledge_context += f"\n[KEDB ENTRY {i+1}]:\n- Known Issue: {inc['issue']}\n- Root Cause: {inc['root_cause']}\n- Proven Resolution: {inc['resolution']}\n"

        system_instruction = Config.SYSTEM_PROMPT
        user_content = f"REFERENCE FROM KNOWN ERROR DATABASE (KEDB):\n{knowledge_context}\n\nNEW INCIDENT TO ANALYZE:\n{query}"

        try:
            with httpx.Client(timeout=30.0) as client:
                response = client.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    headers={"Authorization": f"Bearer {client_key}"},
                    json={
                        "model": Config.MODEL_NAME,
                        "messages": [
                            {"role": "system", "content": system_instruction},
                            {"role": "user", "content": user_content}
                        ],
                        "temperature": Config.TEMPERATURE,
                        "max_tokens": Config.MAX_TOKENS
                    }
                )
                
                if response.status_code == 200:
                    return response.json()['choices'][0]['message']['content']
                return None
        except Exception as e:
            print(f"Expert Engine Error: {str(e)}")
            return None
