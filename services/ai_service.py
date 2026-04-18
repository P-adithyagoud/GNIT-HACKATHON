import os
import httpx
from config import Config

class AIService:
    """
    SRE Expert Engine: Conducts intelligent analysis and knowledge re-ranking.
    """

    @staticmethod
    def generate_resolution_analysis(query, candidate_pool):
        """Generates resolution and ranks the most relevant historical context."""
        client_key = os.getenv("GROQ_API_KEY")
        if not client_key:
            return None

        # Build candidate knowledge base for AI ranking
        candidate_context = ""
        for i, inc in enumerate(candidate_pool):
            # Label the source for better AI understanding
            source = "LOCAL KEDB" if i < 3 else "CLOUD ARCHIVE"
            candidate_context += f"\n[CANDIDATE {i+1} - {source}]:\n- Issue: {inc.get('issue')}\n- Cause: {inc.get('root_cause')}\n- Fix: {inc.get('resolution')}\n"

        system_instruction = Config.SYSTEM_PROMPT
        user_content = f"CANDIDATE HISTORICAL CASES (Analyze and Select Top 3):\n{candidate_context}\n\nCURRENT PRODUCTION ISSUE:\n{query}"

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
