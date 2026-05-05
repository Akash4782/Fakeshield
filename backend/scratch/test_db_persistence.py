import os
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime, timezone

async def test_db_persistence():
    MONGO_URL = os.getenv("MONGO_URL")
    if not MONGO_URL:
        print("Error: MONGO_URL environment variable not set.")
        return
    print("Testing DB persistence...")
    
    # Use short timeout to fail fast if unreachable
    client = AsyncIOMotorClient(MONGO_URL, serverSelectionTimeoutMS=10000)
    db = client.fakeshield_db
    test_col = db.test_connection
    
    try:
        # 1. Ping
        await client.admin.command('ping')
        print("[1/3] Ping SUCCESS!")
        
        # 2. Write
        test_id = f"test_{int(datetime.now().timestamp())}"
        doc = {
            "test_id": test_id,
            "message": "Persistence check",
            "timestamp": datetime.now(timezone.utc)
        }
        await test_col.insert_one(doc)
        print(f"[2/3] Write SUCCESS! (ID: {test_id})")
        
        # 3. Read
        found = await test_col.find_one({"test_id": test_id})
        if found:
            print(f"[3/3] Read SUCCESS! Found record: {found['test_id']}")
            print("\nCONCLUSION: Database is working properly with full Read/Write access.")
        else:
            print("[3/3] Read FAILED! Could not find the record we just wrote.")
            
        # Cleanup
        await test_col.delete_one({"test_id": test_id})
        
    except Exception as e:
        print(f"FAILURE: DB is NOT working properly. Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_db_persistence())
