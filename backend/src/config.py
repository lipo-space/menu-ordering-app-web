from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings"""

    # Supabase Configuration
    SUPABASE_URL: str
    SUPABASE_ANON_KEY: str
    SUPABASE_SERVICE_KEY: str

    # API Configuration
    API_VERSION: str = "v1"
    ENVIRONMENT: str = "development"

    # CORS
    ALLOWED_ORIGINS: str = "http://localhost:5173,http://localhost:3000,https://menu-ordering-app-web.vercel.app,https://*.vercel.app"

    @property
    def allowed_origins_list(self) -> List[str]:
        """Parse allowed origins from comma-separated string"""
        origins = self.ALLOWED_ORIGINS.split(",")
        return [origin.strip() for origin in origins if origin.strip()]

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
