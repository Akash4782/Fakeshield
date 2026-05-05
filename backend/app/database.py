import os
from motor.motor_asyncio import AsyncIOMotorClient
import asyncio

# Load from environment variable for production readiness
# Load from environment variable for security
MONGO_URL = os.getenv("MONGO_URL")

class DummyCollection:
    """Mock collection to prevent crashes when MongoDB is unreachable."""
    def __init__(self, name): 
        self.name = name
    async def create_index(self, *args, **kwargs): return None
    async def insert_one(self, *args, **kwargs): return type('obj', (), {'inserted_id': 'offline_id'})
    async def find_one(self, *args, **kwargs): return None
    def find(self, *args, **kwargs):
        class DummyCursor:
            async def to_list(self, *args, **kwargs): return []
            def sort(self, *args, **kwargs): return self
            def limit(self, *args, **kwargs): return self
        return DummyCursor()

# Global state
client = None
db = None
users_collection = DummyCollection("users")
video_results_collection = DummyCollection("video_forensics")
audio_results_collection = DummyCollection("audio_forensics")
image_results_collection = DummyCollection("image_forensics")
text_results_collection = DummyCollection("text_forensics")

try:
    # Create the Async MongoDB Client with a short timeout
    client = AsyncIOMotorClient(MONGO_URL, serverSelectionTimeoutMS=2000)
    db = client.fakeshield_db
    
    # Real collections (proxies for Atlas)
    users_collection = db.get_collection("users")
    video_results_collection = db.get_collection("video_forensics")
    audio_results_collection = db.get_collection("audio_forensics")
    image_results_collection = db.get_collection("image_forensics")
    text_results_collection = db.get_collection("text_forensics")
    print("[DB] MongoDB Client Initialized (Proxied).")
except Exception as e:
    print(f"[DB] Initial setup error: {e}")

async def init_db():
    """Initializes indexes. Gracefully handles Atlas timeouts."""
    if client is None:
        print("[DB] Skipping Index Initialization (Offline Mode)")
        return

    try:
        # Check connection - if this fails, we stay in Dummy mode
        await client.admin.command('ping')
        
        collections = [
            users_collection, video_results_collection, 
            audio_results_collection, image_results_collection, 
            text_results_collection
        ]
        
        for col in collections:
            if col.name == "users":
                await col.create_index("email", unique=True)
            else:
                await col.create_index("user_email")
            await col.create_index([("created_at", -1)])
        print("[DB] MongoDB Atlas Online: Indexes Initialized!")
    except Exception as e:
        print(f"[DB] Atlas Reachability Check Failed: {e}")
        print("[DB] Operating in Reduced Functional Mode (No Data Persistence).")
