import json

class ResponseParser:
    @staticmethod
    def parse_json(response_text):
        """Attempt to parse valid JSON from response."""
        try:
            # Basic cleanup in case of leading/trailing text
            start = response_text.find('{')
            end = response_text.rfind('}') + 1
            if start != -1 and end != -1:
                response_text = response_text[start:end]
            
            data = json.loads(response_text)
            
            if not isinstance(data, dict):
                return None
            
            # Updated required keys based on the new mandatory format
            required_keys = ['incident_summary', 'root_cause', 'immediate_actions', 'resolution_steps', 'confidence']
            if not all(key in data for key in required_keys):
                print(f"Parser Error: Missing keys. Found {list(data.keys())}")
                return None
            
            # Ensure lists are lists
            if not isinstance(data['immediate_actions'], list) or not isinstance(data['resolution_steps'], list):
                return None
            
            return data
        
        except (json.JSONDecodeError, ValueError, TypeError) as e:
            print(f"Parser Exception: {str(e)}")
            return None
