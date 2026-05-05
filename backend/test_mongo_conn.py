from motor.motor_asyncio import AsyncIOMotorClient
import asyncio

async def test_conn():
    MONGO_URL = "mongodb+srv://fakeshield_admin:fakeshield123@cluster0.uxrdypt.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    client = AsyncIOMotorClient(MONGO_URL, serverSelectionTimeoutMS=5000, tlsAllowInvalidCertificates=True)
    try:
        await client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_conn())
