import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

async def check():
    load_dotenv()
    uri = os.getenv("MONGODB_URI")
    db_name = os.getenv("DB_NAME", "realtime_chat")
    
    print(f"Connecting to: {uri[:20]}...")
    client = AsyncIOMotorClient(uri)
    db = client[db_name]
    
    try:
        # Check connection
        await client.admin.command('ping')
        print("✅ Successfully connected to MongoDB Atlas!")
        
        # Check collections
        collections = await db.list_collection_names()
        print(f"Collections found: {collections}")
        
        for coll_name in collections:
            count = await db[coll_name].count_documents({})
            print(f" - {coll_name}: {count} documents")
            
    except Exception as e:
        print(f"❌ Connection failed: {e}")

if __name__ == "__main__":
    asyncio.run(check())
