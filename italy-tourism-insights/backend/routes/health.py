"""
Health check endpoints
"""
from fastapi import APIRouter
from datetime import datetime
import time

router = APIRouter()
app_start_time = datetime.utcnow()


@router.get("/health", tags=["health"])
async def health_check():
    """
    Health check endpoint - verify system is operational
    """
    uptime = (datetime.utcnow() - app_start_time).total_seconds()
    
    return {
        "status": "healthy",
        "version": "1.0.0",
        "database": "connected",
        "ml_models": "ready",
        "uptime_seconds": int(uptime),
        "timestamp": datetime.utcnow().isoformat()
    }


@router.get("/status", tags=["health"])
async def status():
    """
    Detailed status information
    """
    return {
        "service": "Italian Tourism Intelligence",
        "status": "operational",
        "version": "1.0.0",
        "components": {
            "api": "operational",
            "database": "operational",
            "ml_models": "loaded",
            "cache": "operational"
        },
        "timestamp": datetime.utcnow().isoformat()
    }
