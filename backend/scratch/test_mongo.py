import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

async def test_mongo():
    MONGO_URL = "mongodb+srv://fakeshield_admin:fakeshield123@cluster0.uxrdypt.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    print(f"Connecting to MongoDB...")
    client = AsyncIOMotorClient(MONGO_URL)
    try:
        # The ismaster command is cheap and does not require auth.
        await client.admin.command('ismaster')
        print("MongoDB connection successful!")
        db = client.fakeshield_db
        count = await db.get_collection("users").count_documents({})
        print(f"User count: {count}")
    except Exception as e:
        print(f"MongoDB connection failed: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    asyncio.run(test_mongo())
