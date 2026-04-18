import os
from supabase import create_client, Client
from config import Config

class SupabaseService:
    _client: Client = None

    @classmethod
    def get_client(cls) -> Client:
        """Initialize and return the Supabase client."""
        if cls._client is None:
            if not Config.SUPABASE_URL or not Config.SUPABASE_KEY:
                print("Warning: Supabase credentials not found in environment.")
                return None
            cls._client = create_client(Config.SUPABASE_URL, Config.SUPABASE_KEY)
        return cls._client

    @staticmethod
    def get_all_incidents():
        """Fetch all past incidents from the 'incidents' table."""
        client = SupabaseService.get_client()
        if not client:
            return []
        
        try:
            response = client.table('incidents').select('*').execute()
            return response.data
        except Exception as e:
            print(f"Supabase Fetch Error: {str(e)}")
            return []

    @staticmethod
    def store_incident(issue, root_cause, resolution):
        """Store a new incident in the database."""
        client = SupabaseService.get_client()
        if not client:
            return None
        
        try:
            data = {
                "issue": issue,
                "root_cause": root_cause,
                "resolution": resolution,
                "tags": "analyzed"  # Default tag
            }
            response = client.table('incidents').insert(data).execute()
            return response.data
        except Exception as e:
            print(f"Supabase Store Error: {str(e)}")
            return None
