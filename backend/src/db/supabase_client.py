from supabase import create_client
from ..config import settings

# Initialize Supabase client
supabase = create_client(
    settings.SUPABASE_URL,
    settings.SUPABASE_SERVICE_KEY
)

__all__ = ['supabase']
