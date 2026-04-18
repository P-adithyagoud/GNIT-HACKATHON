import json
import os

class KEDBService:
    """
    Known Error Database Service: Manages local curated static knowledge.
    Ensures 'Gold Standard' fixes are always available even without cloud DB.
    """
    
    _KEDB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'kedb.json')

    @classmethod
    def find_known_errors(cls):
        """Loads and returns the local Known Error Database."""
        if not os.path.exists(cls._KEDB_PATH):
            return []
            
        try:
            with open(cls._KEDB_PATH, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"KEDB Load Error: {str(e)}")
            return []
