from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from config import settings
from database import db
from routers import auth, rides, bookings, dashboard

# Lifespan events
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print(f"🚗 {settings.app_name} v{settings.app_version} Starting...")
    print("📚 API Documentation: http://localhost:8000/docs")
    print("🏥 Health Check: http://localhost:8000/health")
    
    # Create sample data for testing
    print("\n=== Creating Sample Data ===")
    from auth import get_password_hash
    import uuid
    
    sample_users = [
        {
            "email": "john.driver@example.com",
            "username": "johndriver",
            "hashed_password": get_password_hash("password123"),
            "full_name": "John Driver",
            "phone": "+1234567890",
            "role": "driver"
        },
        {
            "email": "jane.passenger@example.com", 
            "username": "janepassenger",
            "hashed_password": get_password_hash("password123"),
            "full_name": "Jane Passenger",
            "phone": "+1234567891",
            "role": "passenger"
        }
    ]
    
    for user_data in sample_users:
        user_id = db.create_user(user_data)
        if user_id:
            print(f"✅ Created user: {user_data['email']}")
        else:
            print(f"ℹ️  User already exists: {user_data['email']}")
    
    print(f"\n🚀 {settings.app_name} Ready!")
    
    yield
    
    # Shutdown
    print(f"\n👋 {settings.app_name} Shutting down...")

# Initialize FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Backend API for Carpool Hub application",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(rides.router)
app.include_router(bookings.router)
app.include_router(dashboard.router)

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": f"Welcome to {settings.app_name}",
        "version": settings.app_version,
        "docs": "/docs"
    }

# Health check endpoint
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "app": settings.app_name,
        "version": settings.app_version
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug
    )