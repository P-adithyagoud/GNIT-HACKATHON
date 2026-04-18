import json
import re

class ResponseParser:
    @staticmethod
    def parse_json(raw_text):
        if not raw_text: return None
        try:
            match = re.search(r'(\{.*\})', raw_text, re.DOTALL)
            return json.loads(match.group(1) if match else raw_text)
        except (json.JSONDecodeError, AttributeError):
            print("Parser: Failed to clean AI response.")
            return None
