"""
Vercel serverless function entry point for FastAPI backend
"""
from mangum import Mangum
from backend.src.api import app

# Export handler for Vercel
handler = Mangum(app, lifespan="off")
