from fastapi import APIRouter, HTTPException, Depends, status
from datetime import timedelta

from models import UserCreate, UserLogin, Token, UserProfile, SuccessResponse
from auth import get_password_hash, authenticate_user, create_access_token, get_current_user
from database import db
from config import settings

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/signup", response_model=SuccessResponse)
async def signup(user: UserCreate):
    # Check if user already exists
    existing_user = db.get_user_by_email(user.email)
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )
    
    # Create new user
    user_data = {
        "email": user.email,
        "username": user.username,
        "hashed_password": get_password_hash(user.password),
        "full_name": user.full_name,
        "phone": user.phone,
        "role": user.role.value
    }
    
    user_id = db.create_user(user_data)
    if user_id is None:
        raise HTTPException(
            status_code=400,
            detail="Username already taken"
        )
    
    return SuccessResponse(
        message="User created successfully",
        data={"user_id": user_id, "email": user.email}
    )

@router.post("/login", response_model=Token)
async def login(user_credentials: UserLogin):
    user = authenticate_user(user_credentials.email, user_credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user["email"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserProfile)
async def read_users_me(current_user: dict = Depends(get_current_user)):
    return UserProfile(**current_user)

@router.post("/logout", response_model=SuccessResponse)
async def logout(current_user: dict = Depends(get_current_user)):
    # In a real application, you might want to blacklist the token
    return SuccessResponse(message="Successfully logged out")