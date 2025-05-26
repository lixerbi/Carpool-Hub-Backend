import sqlite3
import uuid
from typing import Optional, List, Dict, Any
from datetime import datetime

class Database:
    def __init__(self, db_path: str = "carpool_hub.db"):
        self.db_path = db_path
        self.init_db()
    
    def get_connection(self):
        return sqlite3.connect(self.db_path)
    
    def init_db(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY,
                email TEXT UNIQUE NOT NULL,
                username TEXT UNIQUE NOT NULL,
                hashed_password TEXT NOT NULL,
                full_name TEXT NOT NULL,
                phone TEXT,
                profile_image TEXT,
                bio TEXT,
                role TEXT DEFAULT 'both',
                rating REAL DEFAULT 0.0,
                total_rides INTEGER DEFAULT 0,
                is_verified BOOLEAN DEFAULT FALSE,
                is_active BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Rides table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS rides (
                id TEXT PRIMARY KEY,
                driver_id TEXT NOT NULL,
                title TEXT NOT NULL,
                description TEXT,
                origin_address TEXT NOT NULL,
                destination_address TEXT NOT NULL,
                origin_lat REAL,
                origin_lng REAL,
                destination_lat REAL,
                destination_lng REAL,
                departure_time TIMESTAMP NOT NULL,
                available_seats INTEGER NOT NULL,
                price_per_seat REAL NOT NULL,
                status TEXT DEFAULT 'active',
                vehicle_info TEXT,
                preferences TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (driver_id) REFERENCES users (id)
            )
        ''')
        
        # Bookings table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS bookings (
                id TEXT PRIMARY KEY,
                ride_id TEXT NOT NULL,
                passenger_id TEXT NOT NULL,
                seats_booked INTEGER NOT NULL,
                total_price REAL NOT NULL,
                status TEXT DEFAULT 'pending',
                message TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (ride_id) REFERENCES rides (id),
                FOREIGN KEY (passenger_id) REFERENCES users (id)
            )
        ''')
        
        # Reviews table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS reviews (
                id TEXT PRIMARY KEY,
                ride_id TEXT NOT NULL,
                reviewer_id TEXT NOT NULL,
                reviewed_user_id TEXT NOT NULL,
                rating INTEGER NOT NULL,
                comment TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (ride_id) REFERENCES rides (id),
                FOREIGN KEY (reviewer_id) REFERENCES users (id),
                FOREIGN KEY (reviewed_user_id) REFERENCES users (id)
            )
        ''')
        
        # Messages table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id TEXT PRIMARY KEY,
                ride_id TEXT NOT NULL,
                sender_id TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (ride_id) REFERENCES rides (id),
                FOREIGN KEY (sender_id) REFERENCES users (id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    # User operations
    def create_user(self, user_data: Dict[str, Any]) -> Optional[str]:
        conn = self.get_connection()
        cursor = conn.cursor()
        user_id = str(uuid.uuid4())
        
        try:
            cursor.execute(
                """INSERT INTO users (id, email, username, hashed_password, full_name, phone, role) 
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (user_id, user_data["email"], user_data["username"], user_data["hashed_password"],
                 user_data["full_name"], user_data.get("phone"), user_data["role"])
            )
            conn.commit()
            conn.close()
            return user_id
        except sqlite3.IntegrityError:
            conn.close()
            return None
    
    def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()
        conn.close()
        
        if user:
            return {
                "id": user[0], "email": user[1], "username": user[2], "hashed_password": user[3],
                "full_name": user[4], "phone": user[5], "profile_image": user[6], "bio": user[7],
                "role": user[8], "rating": user[9], "total_rides": user[10], "is_verified": user[11],
                "is_active": user[12]
            }
        return None
    
    def get_user_by_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        user = cursor.fetchone()
        conn.close()
        
        if user:
            return {
                "id": user[0], "email": user[1], "username": user[2], "hashed_password": user[3],
                "full_name": user[4], "phone": user[5], "profile_image": user[6], "bio": user[7],
                "role": user[8], "rating": user[9], "total_rides": user[10], "is_verified": user[11],
                "is_active": user[12]
            }
        return None
    
    # Ride operations
    def create_ride(self, ride_data: Dict[str, Any]) -> str:
        conn = self.get_connection()
        cursor = conn.cursor()
        ride_id = str(uuid.uuid4())
        
        cursor.execute(
            """INSERT INTO rides (id, driver_id, title, description, origin_address, destination_address,
               origin_lat, origin_lng, destination_lat, destination_lng, departure_time, available_seats,
               price_per_seat, vehicle_info, preferences) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (ride_id, ride_data["driver_id"], ride_data["title"], ride_data["description"],
             ride_data["origin_address"], ride_data["destination_address"], ride_data.get("origin_lat"),
             ride_data.get("origin_lng"), ride_data.get("destination_lat"), ride_data.get("destination_lng"),
             ride_data["departure_time"], ride_data["available_seats"], ride_data["price_per_seat"],
             ride_data.get("vehicle_info"), ride_data.get("preferences"))
        )
        conn.commit()
        conn.close()
        return ride_id
    
    def search_rides(self, filters: Dict[str, Any]) -> List[Dict[str, Any]]:
        conn = self.get_connection()
        cursor = conn.cursor()
        
        query = """
            SELECT r.*, u.id, u.username, u.full_name, u.rating, u.profile_image
            FROM rides r
            JOIN users u ON r.driver_id = u.id
            WHERE r.status = 'active' AND r.departure_time > datetime('now')
        """
        params = []
        
        if filters.get("origin"):
            query += " AND r.origin_address LIKE ?"
            params.append(f"%{filters['origin']}%")
        if filters.get("destination"):
            query += " AND r.destination_address LIKE ?"
            params.append(f"%{filters['destination']}%")
        if filters.get("date"):
            query += " AND date(r.departure_time) = ?"
            params.append(filters["date"])
        if filters.get("seats"):
            query += " AND r.available_seats >= ?"
            params.append(filters["seats"])
        if filters.get("max_price"):
            query += " AND r.price_per_seat <= ?"
            params.append(filters["max_price"])
        
        query += " ORDER BY r.departure_time ASC"
        
        cursor.execute(query, params)
        rides = cursor.fetchall()
        conn.close()
        
        result = []
        for ride in rides:
            result.append({
                "id": ride[0], "driver_id": ride[1], "title": ride[2], "description": ride[3],
                "origin_address": ride[4], "destination_address": ride[5], "origin_lat": ride[6],
                "origin_lng": ride[7], "destination_lat": ride[8], "destination_lng": ride[9],
                "departure_time": ride[10], "available_seats": ride[11], "price_per_seat": ride[12],
                "status": ride[13], "vehicle_info": ride[14], "preferences": ride[15],
                "driver": {
                    "id": ride[17], "username": ride[18], "full_name": ride[19],
                    "rating": ride[20], "profile_image": ride[21]
                }
            })
        
        return result

# Global database instance
db = Database()