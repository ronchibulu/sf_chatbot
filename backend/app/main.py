"""Main FastAPI application."""
import sys
import asyncio

# Fix for Windows asyncio event loop with psycopg
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.v1.main import router as v1_router

app = FastAPI(
    title="SleekFlow Chatbot API",
    version="0.1.0",
    description="FastAPI backend for SleekFlow Chatbot TODO application"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API v1 router
app.include_router(v1_router)


@app.get("/")
async def root():
    """Root endpoint for health check."""
    return {"message": "SleekFlow Chatbot API is running", "version": "0.1.0"}


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}
