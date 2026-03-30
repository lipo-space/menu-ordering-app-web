from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from ..config import settings

# Create FastAPI app
app = FastAPI(
    title="家庭点菜系统 API",
    description="Family Menu Ordering System Backend API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "家庭点菜系统 API",
        "version": "1.0.0",
        "docs": "/docs",
        "status": "running"
    }


# Health check
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "environment": settings.ENVIRONMENT
    }


# Import and include routers
from . import dishes, menus, combinations

app.include_router(dishes.router, prefix="/api/v1/dishes", tags=["dishes"])
app.include_router(menus.router, prefix="/api/v1/menus", tags=["menus"])
app.include_router(combinations.router, prefix="/api/v1/combinations", tags=["combinations"])
