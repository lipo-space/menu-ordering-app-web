from supabase import create_client, Client
from ..config import settings

# Initialize Supabase client with compatible options
supabase: Client = create_client(
    settings.SUPABASE_URL,
    settings.SUPABASE_SERVICE_KEY,
    options={
        'auto_refresh_token': True,
        'persist_session': True
    }
)

__all__ = ['supabase']
