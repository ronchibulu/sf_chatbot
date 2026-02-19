"""Backend entry point for running with uvicorn."""
import sys
import asyncio
import uvicorn

# Fix for Windows asyncio event loop with psycopg
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
