"""
Vercel serverless function entry point for FastAPI backend
"""
import sys
from pathlib import Path

# Add parent directory to path to import backend modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from mangum import Mangum
from backend.src.api import app

# Vercel requires the handler to be named 'handler'
# Mangum adapts FastAPI (ASGI) to work with AWS Lambda (which Vercel uses)
handler = Mangum(app)
