import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

async def check():
    uri = "mongodb+srv://fakeshield_admin:fakeshield123@cluster0.uxrdypt.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    client = AsyncIOMotorClient(uri)
    dbs = await client.list_database_names()
    print(f"Databases: {dbs}")
    
    for dbname in dbs:
        db = client[dbname]
        cols = await db.list_collection_names()
        print(f"DB '{dbname}' collections: {cols}")

if __name__ == "__main__":
    asyncio.run(check())
