from fastapi import APIRouter, HTTPException, Depends, Query
from typing import Optional, List

from models import RideCreate, RideResponse, SuccessResponse
from auth import get_current_user
from database import db

router = APIRouter(prefix="/rides", tags=["Rides"])

@router.post("", response_model=SuccessResponse)
async def create_ride(ride: RideCreate, current_user: dict = Depends(get_current_user)):
    ride_data = {
        "driver_id": current_user["id"],
        "title": ride.title,
        "description": ride.description,
        "origin_address": ride.origin_address,
        "destination_address": ride.destination_address,
        "origin_lat": ride.origin_lat,
        "origin_lng": ride.origin_lng,
        "destination_lat": ride.destination_lat,
        "destination_lng": ride.destination_lng,
        "departure_time": ride.departure_time,
        "available_seats": ride.available_seats,
        "price_per_seat": ride.price_per_seat,
        "vehicle_info": ride.vehicle_info,
        "preferences": ride.preferences
    }
    
    ride_id = db.create_ride(ride_data)
    return SuccessResponse(
        message="Ride created successfully",
        data={"ride_id": ride_id}
    )

@router.get("", response_model=List[dict])
async def search_rides(
    origin: Optional[str] = Query(None),
    destination: Optional[str] = Query(None),
    date: Optional[str] = Query(None),
    seats: Optional[int] = Query(None),
    max_price: Optional[float] = Query(None)
):
    filters = {
        "origin": origin,
        "destination": destination,
        "date": date,
        "seats": seats,
        "max_price": max_price
    }
    
    # Remove None values
    filters = {k: v for k, v in filters.items() if v is not None}
    
    rides = db.search_rides(filters)
    return rides

@router.get("/{ride_id}")
async def get_ride(ride_id: str):
    # Implementation for getting a specific ride
    # This would need to be added to the database.py file
    pass

@router.get("/user/{user_id}")
async def get_user_rides(user_id: str, current_user: dict = Depends(get_current_user)):
    # Implementation for getting user's rides
    # This would need to be added to the database.py file
    pass