"""Tests for project initialization - Story 1.1"""

import asyncio
import sys
from pathlib import Path

import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy import text

from app.db.session import engine
from app.main import app

# Fix for Windows ProactorEventLoop issue with psycopg
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


class TestProjectInitialization:
    """Tests for Story 1.1: Project Initialization with Starter Template"""

    def test_directory_structure_backend(self):
        """AC 5: Verify backend directory structure matches specification."""
        backend_root = Path(__file__).parent.parent

        # Verify required directories exist
        assert (backend_root / "app").is_dir()
        assert (backend_root / "app" / "api").is_dir()
        assert (backend_root / "app" / "api" / "v1").is_dir()
        assert (backend_root / "app" / "api" / "v1" / "endpoints").is_dir()
        assert (backend_root / "app" / "models").is_dir()
        assert (backend_root / "app" / "schemas").is_dir()
        assert (backend_root / "app" / "services").is_dir()
        assert (backend_root / "app" / "db").is_dir()
        assert (backend_root / "tests").is_dir()
        assert (backend_root / "alembic").is_dir()

        # Verify required files exist
        assert (backend_root / "app" / "main.py").is_file()
        assert (backend_root / "app" / "core" / "config.py").is_file()
        assert (backend_root / "app" / "db" / "session.py").is_file()
        assert (backend_root / "alembic.ini").is_file()
        assert (backend_root / ".env").is_file()
        assert (backend_root / ".env.example").is_file()

    def test_dependencies_installed(self):
        """AC 3: Verify all required backend dependencies are installed."""
        # These imports will fail if dependencies are not installed
        import fastapi
        import sqlmodel
        import alembic
        import pydantic_settings
        import psycopg
        import pytest
        import httpx
        import uvicorn

        # Verify SQLModel version
        assert sqlmodel.__version__ >= "0.0.31"

    @pytest.mark.asyncio
    async def test_database_connectivity(self):
        """AC 8: Verify database connection from backend."""
        async with engine.begin() as conn:
            result = await conn.execute(text("SELECT 1"))
            value = result.scalar()
            assert value == 1

            # Verify database name
            result = await conn.execute(text("SELECT current_database()"))
            db_name = result.scalar()
            assert db_name == "sleekflow_db"

    @pytest.mark.asyncio
    async def test_fastapi_app_starts(self):
        """AC 7: Verify backend dev server can start successfully."""
        # Test that the FastAPI app is properly configured
        assert app.title == "SleekFlow Chatbot API"
        assert app.version == "0.1.0"

        # Test root endpoint
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            response = await client.get("/")
            assert response.status_code == 200
            data = response.json()
            assert data["message"] == "SleekFlow Chatbot API is running"
            assert data["version"] == "0.1.0"

    @pytest.mark.asyncio
    async def test_health_endpoint(self):
        """Test health check endpoint works."""
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            response = await client.get("/health")
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "healthy"

    def test_environment_files_exist(self):
        """AC 6: Verify environment files are created."""
        backend_root = Path(__file__).parent.parent

        assert (backend_root / ".env").is_file()
        assert (backend_root / ".env.example").is_file()

        # Verify .env contains required variables
        env_content = (backend_root / ".env").read_text()
        assert "DATABASE_URL=" in env_content
        assert "SECRET_KEY=" in env_content
        assert "CORS_ORIGINS=" in env_content

    def test_alembic_initialized(self):
        """AC 8: Verify Alembic is initialized."""
        backend_root = Path(__file__).parent.parent

        assert (backend_root / "alembic.ini").is_file()
        assert (backend_root / "alembic").is_dir()
        assert (backend_root / "alembic" / "env.py").is_file()
        assert (backend_root / "alembic" / "versions").is_dir()
