import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

async def check():
    uri = "mongodb+srv://fakeshield_admin:fakeshield123@cluster0.uxrdypt.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    client = AsyncIOMotorClient(uri)
    db = client.fakeshield_db
    col = db.text_forensics
    
    docs = await col.find({}).to_list(length=10)
    for d in docs:
        print(f"Doc: user_email={repr(d.get('user_email'))}, verdict={repr(d.get('verdict'))}")

if __name__ == "__main__":
    asyncio.run(check())
