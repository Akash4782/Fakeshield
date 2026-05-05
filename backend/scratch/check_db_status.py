import os
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

async def check_db_health():
    MONGO_URL = os.getenv("MONGO_URL")
    if not MONGO_URL:
        print("Error: MONGO_URL environment variable not set.")
        return
    print("Connecting to MongoDB...")
    client = AsyncIOMotorClient(MONGO_URL, serverSelectionTimeoutMS=10000, tlsAllowInvalidCertificates=True)
    try:
        # Check if we can reach the server
        await client.admin.command('ping')
        print("SUCCESS: Connected to MongoDB Atlas!")
        
        db = client.fakeshield_db
        collections = await db.list_collection_names()
        print(f"Collections in 'fakeshield_db': {collections}")
        
        for col_name in collections:
            count = await db[col_name].count_documents({})
            print(f" - {col_name}: {count} documents")
            
    except Exception as e:
        print(f"FAILURE: Could not connect to MongoDB. Error: {e}")

if __name__ == "__main__":
    asyncio.run(check_db_health())
