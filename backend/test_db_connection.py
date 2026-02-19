"""Test script to verify database connectivity."""
import asyncio
import sys
from sqlalchemy import text
from app.db.session import engine

# Fix for Windows ProactorEventLoop issue with psycopg
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


async def test_connection():
    """Test PostgreSQL connection."""
    try:
        async with engine.begin() as conn:
            result = await conn.execute(text("SELECT version()"))
            version = result.scalar()
            print("[SUCCESS] Database connection successful!")
            print(f"PostgreSQL version: {version}")
            
            # Test database name
            result = await conn.execute(text("SELECT current_database()"))
            db_name = result.scalar()
            print(f"Connected to database: {db_name}")
            
        return True
    except Exception as e:
        print(f"[ERROR] Database connection failed: {e}")
        return False


if __name__ == "__main__":
    success = asyncio.run(test_connection())
    exit(0 if success else 1)
