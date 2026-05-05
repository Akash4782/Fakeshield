import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

async def run():
    client = AsyncIOMotorClient(os.getenv("MONGODB_URL"))
    db = client.get_database()
    user = await db["users"].find_one()
    if user:
        print(f"USER_EMAIL: {user.get('email')}")
    else:
        print("NO_USER_FOUND")

if __name__ == "__main__":
    asyncio.run(run())
