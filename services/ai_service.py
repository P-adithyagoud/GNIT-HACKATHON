import os
import httpx
from config import Config

class AIService:
    @staticmethod
    def analyze_incident(query, context_incidents):
        client_key = os.getenv("GROQ_API_KEY")
        if not client_key:
            return None

        knowledge_context = ""
        for i, inc in enumerate(context_incidents):
            knowledge_context += f"\n[Case {i+1}]:\nIssue: {inc['issue']}\nRoot Cause: {inc['root_cause']}\nResolution: {inc['resolution']}\n"

        user_content = f"CONTEXT:\n{knowledge_context}\n\nCURRENT ISSUE:\n{query}"

        try:
            with httpx.Client(timeout=30.0) as client:
                response = client.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    headers={"Authorization": f"Bearer {client_key}"},
                    json={
                        "model": Config.MODEL_NAME,
                        "messages": [
                            {"role": "system", "content": Config.SYSTEM_PROMPT},
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
            print(f"AI Error: {str(e)}")
            return None
