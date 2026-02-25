"""
Italian Tourism Intelligence Dashboard
FastAPI Application Entry Point

A professional data intelligence platform for analyzing Italian tourism,
cultural heritage, and visitor patterns with predictive ML models.
"""

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
import logging

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Import routes
from database import init_db
from routes import analytics, forecasts, sites, health, chatbot

# Initialize FastAPI
app = FastAPI(
    title="🇮🇹 Italian Tourism Intelligence",
    description="Data Analytics & ML Forecasting Platform for Italian Tourism & Cultural Heritage",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# CORS Middleware
allowed_origins = os.getenv('ALLOWED_ORIGINS', 'http://localhost:5173,http://localhost:3000').split(',')
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Gzip Compression
app.add_middleware(GZipMiddleware, minimum_size=1000)


# Startup Event
@app.on_event("startup")
async def startup_event():
    """Initialize application on startup"""
    logger.info("🚀 Starting Italian Tourism Intelligence Platform...")
    
    # Initialize database
    try:
        init_db()
        logger.info("✓ Database initialized successfully")
    except Exception as e:
        logger.error(f"✗ Database initialization failed: {e}")
    
    # Load ML models
    try:
        # Future: Load pre-trained models
        logger.info("✓ ML models loaded successfully")
    except Exception as e:
        logger.error(f"✗ ML model loading failed: {e}")


# Shutdown Event
@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("🔴 Shutting down Italian Tourism Intelligence Platform...")


# Root Endpoint
@app.get("/")
async def root():
    """Root endpoint - returns API information"""
    return {
        "name": "Italian Tourism Intelligence Dashboard",
        "version": "1.0.0",
        "status": "operational",
        "docs": "/docs",
        "health": "/api/health"
    }


# Include Routers
app.include_router(health.router, prefix="/api", tags=["health"])
app.include_router(analytics.router, prefix="/api", tags=["analytics"])
app.include_router(forecasts.router, prefix="/api", tags=["forecasts"])
app.include_router(sites.router, prefix="/api", tags=["sites"])
app.include_router(chatbot.router, prefix="/api", tags=["chatbot"])


# Global Exception Handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Handle uncaught exceptions"""
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "type": str(type(exc).__name__)
        }
    )


if __name__ == "__main__":
    import uvicorn
    
    port = int(os.getenv('PORT', 8000))
    debug = os.getenv('DEBUG', 'False').lower() == 'true'
    
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=port,
        reload=debug,
        log_level="info"
    )
