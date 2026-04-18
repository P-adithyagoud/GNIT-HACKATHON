import httpx
from config import Config

class AIService:
    @staticmethod
    def analyze_incident(incident_text, similar_incidents=None):
        """Call Groq API with incident details and historical context."""
        if not Config.GROQ_API_KEY:
            return None
        
        # Prepare context from similar incidents
        context_str = ""
        if similar_incidents:
            context_str = "\n\n### Similar Past Incidents for Context:\n"
            for i, inc in enumerate(similar_incidents, 1):
                context_str += f"\nIncident {i}:\nIssue: {inc.get('issue')}\nRoot Cause: {inc.get('root_cause')}\nResolution: {inc.get('resolution')}\n"

        user_content = f"Current Incident:\n{incident_text}{context_str}"
        
        try:
            with httpx.Client(timeout=15.0) as client:
                response = client.post(
                    Config.GROQ_API_URL,
                    headers={
                        'Authorization': f'Bearer {Config.GROQ_API_KEY}',
                        'Content-Type': 'application/json'
                    },
                    json={
                        'model': Config.MODEL_NAME,
                        'messages': [
                            {
                                'role': 'system',
                                'content': Config.SYSTEM_PROMPT
                            },
                            {
                                'role': 'user',
                                'content': user_content
                            }
                        ],
                        'temperature': Config.TEMPERATURE,
                        'max_tokens': Config.MAX_TOKENS
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if 'choices' in data and len(data['choices']) > 0:
                        content = data['choices'][0]['message']['content']
                        print(f"AI Service Success: {len(content)} chars")
                        return content
                
                print(f"AI Service API Error: {response.status_code} - {response.text}")
                return None
        
        except Exception as e:
            print(f"AI Service Exception: {str(e)}")
            return None
