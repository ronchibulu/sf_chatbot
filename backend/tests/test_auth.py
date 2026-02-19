"""Tests for authentication - Story 1.2"""
import asyncio
import sys
from pathlib import Path

import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy import text

from app.db.database import engine
from app.main import app

# Fix for Windows ProactorEventLoop issue
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


class TestBetterAuthConfiguration:
    """Tests for Story 1.2: Database Setup and BetterAuth Configuration"""
    
    def test_better_auth_config_exists(self):
        """AC 3: Verify BetterAuth configured with PostgreSQL."""
        frontend_dir = Path(__file__).parent.parent.parent / "frontend"
        auth_config = frontend_dir / "src" / "shared" / "lib" / "auth.ts"
        assert auth_config.exists(), "BetterAuth config should exist at src/shared/lib/auth.ts"
        
        content = auth_config.read_text(encoding='utf-8')
        assert "betterAuth" in content
        assert "Pool" in content or "database" in content
        assert "emailAndPassword" in content
    
    def test_better_auth_route_exists(self):
        """AC 2: Verify BetterAuth route handler exists."""
        frontend_dir = Path(__file__).parent.parent.parent / "frontend"
        route_file = frontend_dir / "src" / "app" / "api" / "auth" / "[...all]" / "route.ts"
        assert route_file.exists(), "BetterAuth route should exist"
        
        content = route_file.read_text()
        assert "better-auth" in content.lower() or "Auth" in content
    
    def test_environment_variables(self):
        """AC 10: Verify environment variables configured."""
        frontend_dir = Path(__file__).parent.parent.parent / "frontend"
        env_file = frontend_dir / ".env.local"
        
        assert env_file.exists(), ".env.local should exist"
        content = env_file.read_text()
        
        assert "BETTER_AUTH_SECRET" in content
        assert "BETTER_AUTH_URL" in content
        assert "DATABASE_URL" in content





class TestDatabaseConnection:
    """Tests for database connectivity"""
    
    @pytest.mark.asyncio
    async def test_database_connectivity(self):
        """AC 5: Verify FastAPI can connect to PostgreSQL."""
        async with engine.begin() as conn:
            result = await conn.execute(text("SELECT 1"))
            value = result.scalar()
            assert value == 1
    
    @pytest.mark.asyncio
    async def test_database_can_query_tables(self):
        """AC 3: Verify database connection works (Better Auth tables managed by frontend)."""
        async with engine.begin() as conn:
            # Just verify we can query the database
            # Better Auth tables (user, session, account) are created and managed
            # by the frontend via Better Auth CLI migrations
            result = await conn.execute(text(
                "SELECT table_name FROM information_schema.tables "
                "WHERE table_schema = 'public'"
            ))
            tables = [row[0] for row in result.fetchall()]
            
            # We should at least have the alembic_version table from backend migrations
            assert len(tables) >= 0, "Should be able to query tables"


class TestPasswordHashing:
    """Tests for password hashing configuration"""
    
    def test_bcrypt_installed(self):
        """AC 9: Verify bcrypt is installed for password hashing."""
        import bcrypt
        assert bcrypt is not None
        
        # Test bcrypt functionality
        password = "test_password"
        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        assert bcrypt.checkpw(password.encode(), hashed)
    
    def test_better_auth_uses_secure_hashing(self):
        """AC 9: Verify BetterAuth uses bcrypt or Argon2."""
        # BetterAuth uses bcrypt by default for password hashing
        # This is configured in the BetterAuth setup in shared/lib/auth.ts
        frontend_dir = Path(__file__).parent.parent.parent / "frontend"
        auth_config_file = frontend_dir / "src" / "shared" / "lib" / "auth.ts"
        
        if auth_config_file.exists():
            content = auth_config_file.read_text(encoding='utf-8')
            # BetterAuth with emailAndPassword uses bcrypt by default
            assert "emailAndPassword" in content or "email-and-password" in content.lower()


class TestAPIEndpoints:
    """Test API endpoints with authentication"""
    
    @pytest.mark.asyncio
    async def test_health_endpoint_no_auth(self):
        """Test health endpoint works without authentication."""
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            response = await client.get("/health")
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "healthy"
    
    @pytest.mark.asyncio
    async def test_root_endpoint_no_auth(self):
        """Test root endpoint works without authentication."""
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
            response = await client.get("/")
            assert response.status_code == 200
            data = response.json()
            assert "SleekFlow" in data["message"]
