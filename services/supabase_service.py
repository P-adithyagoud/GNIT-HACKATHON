import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

class SupabaseService:
    _client = None

    @classmethod
    def get_client(cls) -> Client:
        if cls._client is None:
            url = os.getenv("SUPABASE_URL")
            key = os.getenv("SUPABASE_KEY")
            if url and key:
                cls._client = create_client(url, key)
        return cls._client

    @classmethod
    def get_all_incidents(cls):
        client = cls.get_client()
        if not client: return []
        try:
            response = client.table('incidents').select('*').execute()
            return response.data
        except Exception as e:
            print(f"DB Error: {str(e)}")
            return []

    @classmethod
    def store_incident(cls, issue, root_cause, resolution):
        client = cls.get_client()
        if not client: return None
        try:
            data = {"issue": issue, "root_cause": root_cause, "resolution": resolution}
            return client.table('incidents').insert(data).execute().data
        except Exception as e:
            print(f"DB Error: {str(e)}")
            return None
