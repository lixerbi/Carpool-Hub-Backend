from pydantic import BaseModel, EmailStr, validator
from datetime import datetime
from typing import Optional, List
from enum import Enum

class RideStatus(str, Enum):
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class BookingStatus(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"

class UserRole(str, Enum):
    DRIVER = "driver"
    PASSENGER = "passenger"
    BOTH = "both"

# User models
class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str
    full_name: str
    phone: Optional[str] = None
    role: UserRole = UserRole.BOTH

class UserLogin(BaseModel):
    email: str
    password: str

class UserProfile(BaseModel):
    id: str
    email: str
    username: str
    full_name: str
    phone: Optional[str]
    profile_image: Optional[str]
    bio: Optional[str]
    role: str
    rating: float
    total_rides: int
    is_verified: bool

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None
    bio: Optional[str] = None
    profile_image: Optional[str] = None

# Ride models
class RideCreate(BaseModel):
    title: str
    description: Optional[str]
    origin_address: str
    destination_address: str
    origin_lat: Optional[float]
    origin_lng: Optional[float]
    destination_lat: Optional[float]
    destination_lng: Optional[float]
    departure_time: datetime
    available_seats: int
    price_per_seat: float
    vehicle_info: Optional[str]
    preferences: Optional[str]

class RideResponse(BaseModel):
    id: str
    driver: UserProfile
    title: str
    description: Optional[str]
    origin_address: str
    destination_address: str
    departure_time: datetime
    available_seats: int
    price_per_seat: float
    status: str
    vehicle_info: Optional[str]
    preferences: Optional[str]
    created_at: datetime

class RideUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    departure_time: Optional[datetime] = None
    available_seats: Optional[int] = None
    price_per_seat: Optional[float] = None
    vehicle_info: Optional[str] = None
    preferences: Optional[str] = None

# Booking models
class BookingCreate(BaseModel):
    ride_id: str
    seats_booked: int
    message: Optional[str]

class BookingResponse(BaseModel):
    id: str
    ride: RideResponse
    passenger: UserProfile
    seats_booked: int
    total_price: float
    status: str
    message: Optional[str]
    created_at: datetime

# Review models
class ReviewCreate(BaseModel):
    ride_id: str
    reviewed_user_id: str
    rating: int
    comment: Optional[str]
    
    @validator('rating')
    def rating_must_be_valid(cls, v):
        if v < 1 or v > 5:
            raise ValueError('Rating must be between 1 and 5')
        return v

class ReviewResponse(BaseModel):
    id: str
    reviewer: UserProfile
    reviewed_user: UserProfile
    rating: int
    comment: Optional[str]
    created_at: datetime

# Message models
class MessageCreate(BaseModel):
    ride_id: str
    content: str

class MessageResponse(BaseModel):
    id: str
    sender: UserProfile
    content: str
    created_at: datetime

# Token models
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

# Response models
class SuccessResponse(BaseModel):
    message: str
    data: Optional[dict] = None

class ErrorResponse(BaseModel):
    detail: str
    error_code: Optional[str] = None

# Dashboard models
class DashboardStats(BaseModel):
    rides_as_driver: int
    rides_as_passenger: int
    pending_bookings: int
    total_rating: float
    total_rides: int