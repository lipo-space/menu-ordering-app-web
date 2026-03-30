"""
Vercel serverless entry point
"""
from mangum import Mangum
from src.api import app

# Export handler for Vercel
handler = Mangum(app, lifespan="off")
