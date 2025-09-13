from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from config.config import DB_URL, DATABASE_NAME
from typing import Optional

# Global variables for database connection
client: Optional[AsyncIOMotorClient] = None
db: Optional[AsyncIOMotorDatabase] = None

def connect_to_mongo() -> None:
    """Establish connection to MongoDB"""
    global client, db
    try:
        client = AsyncIOMotorClient(DB_URL)
        db = client[DATABASE_NAME]
        print(f"✅ Connected to MongoDB: {DATABASE_NAME}")
    except Exception as e:
        print(f"❌ Failed to connect to MongoDB: {e}")
        raise

def close_mongo_connection() -> None:
    """Close MongoDB connection"""
    global client
    if client:
        client.close()
        print("🔌 MongoDB connection closed")

# Initialize database connection immediately
connect_to_mongo()
