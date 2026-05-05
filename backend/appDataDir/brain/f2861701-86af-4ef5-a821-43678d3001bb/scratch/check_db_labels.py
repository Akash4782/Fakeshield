import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient

async def check():
    uri = "mongodb+srv://fakeshield_admin:fakeshield123@cluster0.uxrdypt.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    client = AsyncIOMotorClient(uri)
    db = client.fakeshield_db
    
    cols = ["text_forensics", "image_forensics", "audio_forensics", "video_forensics"]
    for cname in cols:
        col = db[cname]
        verdicts = await col.distinct("verdict")
        count = await col.count_documents({})
        print(f"Collection {cname}: {count} docs, Unique verdicts: {verdicts}")

if __name__ == "__main__":
    asyncio.run(check())
