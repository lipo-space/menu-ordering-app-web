"""
Vercel serverless function entry point for FastAPI backend
"""
import sys
from pathlib import Path

# Add parent directory to path to import backend modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.src.api import app

# Vercel requires the handler to be named 'handler'
# FastAPI apps are ASGI applications and work directly with Vercel
handler = app
