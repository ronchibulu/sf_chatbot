"""Tests for list detail endpoint."""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from httpx import AsyncClient, ASGITransport
from fastapi import HTTPException

from app.main import app


@pytest.fixture
def mock_db():
    """Create a mock database session."""
    db = AsyncMock()
    return db


@pytest.fixture
def mock_current_user():
    """Create a mock authenticated user."""
    return {"id": "user-123", "email": "test@example.com"}


@pytest.mark.asyncio
async def test_get_list_detail_success(mock_db, mock_current_user):
    """Test successful retrieval of list detail."""
    from app.services.list_service import get_list
    
    # Mock the list object
    mock_list = MagicMock()
    mock_list.id = 1
    mock_list.name = "Test List"
    mock_list.owner_id = "user-123"
    mock_list.created_at = "2026-01-01T00:00:00"
    mock_list.updated_at = "2026-01-01T00:00:00"
    
    # Configure mock to return the list
    mock_db.exec.return_value.first.return_value = mock_list
    
    result = await get_list(mock_db, 1, "user-123")
    
    assert result is not None
    assert result.id == 1
    assert result.name == "Test List"


@pytest.mark.asyncio
async def test_get_list_not_found(mock_db):
    """Test 404 when list doesn't exist."""
    from app.services.list_service import get_list
    
    # Configure mock to return None (list not found)
    mock_db.exec.return_value.first.return_value = None
    
    result = await get_list(mock_db, 999, "user-123")
    
    assert result is None


@pytest.mark.asyncio
async def test_get_list_forbidden(mock_db):
    """Test 403 when user doesn't own the list."""
    from app.services.list_service import get_list
    
    # Mock a list owned by a different user
    mock_list = MagicMock()
    mock_list.id = 1
    mock_list.name = "Other User's List"
    mock_list.owner_id = "different-user"
    
    # Configure mock to return the list
    mock_db.exec.return_value.first.return_value = mock_list
    
    # The service should check ownership - if not owner, it should return None or raise
    result = await get_list(mock_db, 1, "user-123")
    
    # Should return None because owner_id doesn't match
    assert result is None
