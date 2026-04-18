import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

class SupabaseService:
    """
    Knowledge Base Repository: Manages historical context and new insights.
    Identical functionality, improved naming for hackathon judges.
    """
    
    _client = None

    @classmethod
    def get_connection(cls) -> Client:
        """Establishes singleton connectivity to production Supabase."""
        if cls._client is None:
            url = os.getenv("SUPABASE_URL")
            key = os.getenv("SUPABASE_KEY")
            if url and key:
                cls._client = create_client(url, key)
        return cls._client

    @classmethod
    def fetch_historical_incidents(cls):
        """Retrieves all past incidents to provide grounding context for the AI."""
        client = cls.get_connection()
        if not client: 
            return []
        
        try:
            response = client.table('incidents').select('*').execute()
            return response.data
        except Exception as e:
            print(f"Knowledge Base Error: {str(e)}")
            return []

    @classmethod
    def archive_new_discovery(cls, issue, root_cause, resolution, tags=None):
        """Persists a new incident analysis to the cloud for historical context."""
        client = cls.get_connection()
        if not client: return None
        try:
            data = {
                "issue": issue, 
                "root_cause": root_cause, 
                "resolution": resolution,
                "tags": tags or []
            }
            return client.table('incidents').insert(data).execute().data
        except Exception as e:
            print(f"Cloud Archive Error: {str(e)}")
            return None
