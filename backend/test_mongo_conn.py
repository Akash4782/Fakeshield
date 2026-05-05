import os
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

async def test_conn():
    MONGO_URL = os.getenv("MONGO_URL")
    if not MONGO_URL:
        print("Error: MONGO_URL environment variable not set.")
        return
    client = AsyncIOMotorClient(MONGO_URL, serverSelectionTimeoutMS=5000, tlsAllowInvalidCertificates=True)
    try:
        await client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_conn())
