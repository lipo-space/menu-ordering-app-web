from supabase import create_client, Client
from ..config import settings

# Initialize Supabase client
# Using simple initialization for Vercel compatibility
supabase: Client = create_client(
    settings.SUPABASE_URL,
    settings.SUPABASE_SERVICE_KEY
)

__all__ = ['supabase']
