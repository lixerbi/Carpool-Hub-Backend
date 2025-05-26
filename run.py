#!/usr/bin/env python3
"""
Carpool Hub Backend Runner
Run this file to start the development server
"""

import uvicorn
from config import settings

if __name__ == "__main__":
    print(f"🚗 Starting {settings.app_name} Development Server")
    print(f"📍 Environment: {'Development' if settings.debug else 'Production'}")
    print(f"🌐 CORS Origins: {settings.allowed_origins}")
    print("=" * 50)
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
        log_level="info" if settings.debug else "warning"
    )