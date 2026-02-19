"""Tests for TODO items endpoints."""
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


@pytest.fixture
def mock_list():
    """Create a mock TodoList object."""
    mock_list = MagicMock()
    mock_list.id = 1
    mock_list.name = "Test List"
    mock_list.owner_id = "user-123"
    mock_list.created_at = "2026-01-01T00:00:00"
    mock_list.updated_at = "2026-01-01T00:00:00"
    return mock_list


@pytest.mark.asyncio
async def test_create_item_success(mock_db, mock_current_user, mock_list):
    """Test successful creation of a TODO item."""
    from app.services.item_service import create_item
    
    # Configure mock to return a created item
    mock_db.commit = AsyncMock()
    mock_db.refresh = AsyncMock()
    
    # Mock the item returned
    created_item = MagicMock()
    created_item.id = 1
    created_item.list_id = 1
    created_item.text = "Test task"
    created_item.status = "not_started"
    created_item.created_by = "user-123"
    created_item.created_at = "2026-01-01T00:00:00"
    created_item.updated_at = "2026-01-01T00:00:00"
    
    # Mock db.add to set the item
    def mock_add(item):
        pass
    
    mock_db.add = mock_add
    
    result = await create_item(mock_db, 1, "Test task", "user-123")
    
    # Verify item was added and committed
    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()


@pytest.mark.asyncio
async def test_get_items_by_list(mock_db, mock_list):
    """Test getting items by list ID."""
    from app.services.item_service import get_items_by_list
    
    # Mock items
    mock_item1 = MagicMock()
    mock_item1.id = 1
    mock_item1.list_id = 1
    mock_item1.text = "Task 1"
    mock_item1.status = "not_started"
    
    mock_item2 = MagicMock()
    mock_item2.id = 2
    mock_item2.list_id = 1
    mock_item2.text = "Task 2"
    mock_item2.status = "completed"
    
    # Configure mock
    mock_db.execute.return_value.scalars.return_value.all.return_value = [mock_item1, mock_item2]
    
    result = await get_items_by_list(mock_db, 1)
    
    assert len(result) == 2


@pytest.mark.asyncio
async def test_create_item_empty_text_validation():
    """Test that empty text is rejected."""
    from app.schemas.todo_item import TodoItemCreate
    from pydantic import ValidationError
    
    with pytest.raises(ValidationError):
        TodoItemCreate(text="")


@pytest.mark.asyncio
async def test_create_item_whitespace_only_validation():
    """Test that whitespace-only text is rejected at schema level."""
    from app.schemas.todo_item import TodoItemCreate
    from pydantic import ValidationError
    
    # Pydantic's min_length=1 should handle this
    with pytest.raises(ValidationError):
        TodoItemCreate(text="   ")


@pytest.mark.asyncio
async def test_create_item_max_length_validation():
    """Test that text exceeding 500 characters is rejected."""
    from app.schemas.todo_item import TodoItemCreate
    from pydantic import ValidationError
    
    with pytest.raises(ValidationError):
        TodoItemCreate(text="a" * 501)


@pytest.mark.asyncio
async def test_update_item_text_success(mock_db, mock_current_user, mock_list):
    """Test successful update of item text."""
    from app.services.item_service import update_item_text
    
    # Mock item
    mock_item = MagicMock()
    mock_item.id = 1
    mock_item.list_id = 1
    mock_item.text = "Old text"
    mock_item.status = "not_started"
    mock_item.created_by = "user-123"
    
    # Configure mock
    mock_db.execute.return_value.scalars.return_value.first.side_effect = [mock_item, mock_list]
    mock_db.commit = AsyncMock()
    mock_db.refresh = AsyncMock()
    
    result = await update_item_text(mock_db, 1, "New text", "user-123")
    
    # Verify item was updated
    assert result is not None
    assert result.text == "New text"
    mock_db.commit.assert_called_once()


@pytest.mark.asyncio
async def test_update_item_text_not_found(mock_db, mock_current_user):
    """Test update returns None when item doesn't exist."""
    from app.services.item_service import update_item_text
    
    # Configure mock to return None
    mock_db.execute.return_value.scalars.return_value.first.return_value = None
    
    result = await update_item_text(mock_db, 999, "New text", "user-123")
    
    assert result is None


@pytest.mark.asyncio
async def test_update_item_text_no_permission(mock_db, mock_current_user):
    """Test update returns None when user doesn't have permission."""
    from app.services.item_service import update_item_text
    
    # Mock item
    mock_item = MagicMock()
    mock_item.id = 1
    mock_item.list_id = 1
    
    # Mock list owned by different user
    mock_list_other = MagicMock()
    mock_list_other.id = 1
    mock_list_other.owner_id = "different-user"
    
    # Configure mock
    mock_db.execute.return_value.scalars.return_value.first.side_effect = [mock_item, mock_list_other]
    
    result = await update_item_text(mock_db, 1, "New text", "user-123")
    
    assert result is None


@pytest.mark.asyncio
async def test_toggle_item_completion_success(mock_db, mock_current_user, mock_list):
    """Test successful toggle of item completion status."""
    from app.services.item_service import toggle_item_completion
    
    # Mock item - initially not_started
    mock_item = MagicMock()
    mock_item.id = 1
    mock_item.list_id = 1
    mock_item.text = "Test task"
    mock_item.status = "not_started"  # Initially not_started
    mock_item.created_by = "user-123"
    
    # Configure mock
    mock_db.execute.return_value.scalars.return_value.first.side_effect = [mock_item, mock_list]
    mock_db.commit = AsyncMock()
    mock_db.refresh = AsyncMock()
    
    result, error = await toggle_item_completion(mock_db, 1, "user-123")
    
    # Verify item was toggled
    assert result is not None
    assert error is None
    assert result.status == "completed"  # Should be toggled to completed
    mock_db.commit.assert_called_once()


@pytest.mark.asyncio
async def test_toggle_item_completion_untoggle(mock_db, mock_current_user, mock_list):
    """Test toggling a completed item back to not_started."""
    from app.services.item_service import toggle_item_completion
    
    # Mock item - initially completed
    mock_item = MagicMock()
    mock_item.id = 1
    mock_item.list_id = 1
    mock_item.text = "Test task"
    mock_item.status = "completed"  # Initially completed
    mock_item.created_by = "user-123"
    
    # Configure mock
    mock_db.execute.return_value.scalars.return_value.first.side_effect = [mock_item, mock_list]
    mock_db.commit = AsyncMock()
    mock_db.refresh = AsyncMock()
    
    result, error = await toggle_item_completion(db=mock_db, item_id=1, user_id="user-123")
    
    # Verify item was toggled back
    assert result is not None
    assert error is None
    assert result.status == "not_started"  # Should be toggled back to not_started
    mock_db.commit.assert_called_once()


@pytest.mark.asyncio
async def test_toggle_item_completion_not_found(mock_db, mock_current_user):
    """Test toggle returns not_found error when item doesn't exist."""
    from app.services.item_service import toggle_item_completion
    
    # Configure mock to return None (item not found)
    mock_db.execute.return_value.scalars.return_value.first.return_value = None
    
    result, error = await toggle_item_completion(mock_db, 999, "user-123")
    
    assert result is None
    assert error == "not_found"


@pytest.mark.asyncio
async def test_toggle_item_completion_no_permission(mock_db, mock_current_user):
    """Test toggle returns forbidden error when user doesn't have permission."""
    from app.services.item_service import toggle_item_completion
    
    # Mock item
    mock_item = MagicMock()
    mock_item.id = 1
    mock_item.list_id = 1
    
    # Mock list owned by different user
    mock_list_other = MagicMock()
    mock_list_other.id = 1
    mock_list_other.owner_id = "different-user"
    
    # Configure mock
    mock_db.execute.return_value.scalars.return_value.first.side_effect = [mock_item, mock_list_other]
    
    result, error = await toggle_item_completion(mock_db, 1, "user-123")
    
    assert result is None
    assert error == "forbidden"


@pytest.mark.asyncio
async def test_delete_item_success(mock_db, mock_current_user, mock_list):
    """Test successful deletion of an item."""
    from app.services.item_service import delete_item
    from datetime import datetime, timezone
    
    # Mock item
    mock_item = MagicMock()
    mock_item.id = 1
    mock_item.list_id = 1
    mock_item.text = "Test task"
    mock_item.status = "not_started"
    mock_item.deleted_at = None
    
    # Configure mock
    mock_db.execute.return_value.scalars.return_value.first.side_effect = [mock_item, mock_list]
    mock_db.commit = AsyncMock()
    mock_db.add = MagicMock()
    
    result, error = await delete_item(mock_db, 1, "user-123")
    
    # Verify item was soft-deleted
    assert result is True
    assert error is None
    assert mock_item.deleted_at is not None
    mock_db.commit.assert_called_once()


@pytest.mark.asyncio
async def test_delete_item_not_found(mock_db, mock_current_user):
    """Test delete returns not_found error when item doesn't exist."""
    from app.services.item_service import delete_item
    
    # Configure mock to return None
    mock_db.execute.return_value.scalars.return_value.first.return_value = None
    
    result, error = await delete_item(mock_db, 999, "user-123")
    
    assert result is False
    assert error == "not_found"


@pytest.mark.asyncio
async def test_delete_item_no_permission(mock_db, mock_current_user):
    """Test delete returns forbidden when user doesn't have permission."""
    from app.services.item_service import delete_item
    
    # Mock item
    mock_item = MagicMock()
    mock_item.id = 1
    mock_item.list_id = 1
    
    # Mock list owned by different user
    mock_list_other = MagicMock()
    mock_list_other.id = 1
    mock_list_other.owner_id = "different-user"
    
    # Configure mock
    mock_db.execute.return_value.scalars.return_value.first.side_effect = [mock_item, mock_list_other]
    
    result, error = await delete_item(mock_db, 1, "user-123")
    
    assert result is False
    assert error == "forbidden"


@pytest.mark.asyncio
async def test_restore_item_success(mock_db, mock_current_user, mock_list):
    """Test successful restoration of a deleted item."""
    from app.services.item_service import restore_item
    from datetime import datetime, timezone, timedelta
    
    # Mock item - recently deleted
    mock_item = MagicMock()
    mock_item.id = 1
    mock_item.list_id = 1
    mock_item.text = "Test task"
    mock_item.status = "not_started"
    mock_item.deleted_at = datetime.now(timezone.utc)  # Deleted just now
    
    # Configure mock
    mock_db.execute.return_value.scalars.return_value.first.side_effect = [mock_item, mock_list]
    mock_db.commit = AsyncMock()
    mock_db.refresh = AsyncMock()
    mock_db.add = MagicMock()
    
    result, error = await restore_item(mock_db, 1, "user-123")
    
    # Verify item was restored
    assert result is not None
    assert error is None
    assert mock_item.deleted_at is None
    mock_db.commit.assert_called_once()


@pytest.mark.asyncio
async def test_restore_item_not_found(mock_db, mock_current_user):
    """Test restore returns not_found when item doesn't exist."""
    from app.services.item_service import restore_item
    
    # Configure mock to return None
    mock_db.execute.return_value.scalars.return_value.first.return_value = None
    
    result, error = await restore_item(mock_db, 999, "user-123")
    
    assert result is None
    assert error == "not_found"


@pytest.mark.asyncio
async def test_restore_item_timeout(mock_db, mock_current_user, mock_list):
    """Test restore returns timeout error when undo window has passed."""
    from app.services.item_service import restore_item
    from datetime import datetime, timezone, timedelta
    
    # Mock item - deleted more than 5 seconds ago
    mock_item = MagicMock()
    mock_item.id = 1
    mock_item.list_id = 1
    mock_item.deleted_at = datetime.now(timezone.utc) - timedelta(seconds=10)  # 10 seconds ago
    
    # Configure mock
    mock_db.execute.return_value.scalars.return_value.first.side_effect = [mock_item, mock_list]
    
    result, error = await restore_item(mock_db, 1, "user-123")
    
    assert result is None
    assert error == "undo_timeout"


@pytest.mark.asyncio
async def test_restore_item_not_deleted(mock_db, mock_current_user):
    """Test restore returns not_deleted when item wasn't deleted."""
    from app.services.item_service import restore_item
    
    # Mock item - not deleted
    mock_item = MagicMock()
    mock_item.id = 1
    mock_item.deleted_at = None
    
    # Configure mock
    mock_db.execute.return_value.scalars.return_value.first.return_value = mock_item
    
    result, error = await restore_item(mock_db, 1, "user-123")
    
    assert result is None
    assert error == "not_deleted"


# ============== Tests for Story 3-5: Due Date and Priority ==============

@pytest.mark.asyncio
async def test_set_item_due_date_success(mock_db, mock_current_user, mock_list):
    """Test successful setting of item due date."""
    from app.services.item_service import set_item_due_date
    from datetime import date
    
    # Mock item
    mock_item = MagicMock()
    mock_item.id = 1
    mock_item.list_id = 1
    mock_item.text = "Test task"
    mock_item.status = "not_started"
    mock_item.due_date = None
    
    # Configure mock
    mock_db.execute.return_value.scalars.return_value.first.side_effect = [mock_item, mock_list]
    mock_db.commit = AsyncMock()
    mock_db.refresh = AsyncMock()
    mock_db.add = MagicMock()
    
    test_date = date(2026, 3, 15)
    result, error = await set_item_due_date(mock_db, 1, test_date, "user-123")
    
    # Verify due date was set
    assert result is not None
    assert error is None
    assert result.due_date == test_date
    mock_db.commit.assert_called_once()


@pytest.mark.asyncio
async def test_set_item_due_date_clear(mock_db, mock_current_user, mock_list):
    """Test clearing item due date."""
    from app.services.item_service import set_item_due_date
    from datetime import date
    
    # Mock item with existing due date
    mock_item = MagicMock()
    mock_item.id = 1
    mock_item.list_id = 1
    mock_item.text = "Test task"
    mock_item.status = "not_started"
    mock_item.due_date = date(2026, 3, 15)
    
    # Configure mock
    mock_db.execute.return_value.scalars.return_value.first.side_effect = [mock_item, mock_list]
    mock_db.commit = AsyncMock()
    mock_db.refresh = AsyncMock()
    mock_db.add = MagicMock()
    
    result, error = await set_item_due_date(mock_db, 1, None, "user-123")
    
    # Verify due date was cleared
    assert result is not None
    assert error is None
    assert result.due_date is None
    mock_db.commit.assert_called_once()


@pytest.mark.asyncio
async def test_set_item_due_date_not_found(mock_db, mock_current_user):
    """Test set due date returns not_found when item doesn't exist."""
    from app.services.item_service import set_item_due_date
    
    # Configure mock to return None
    mock_db.execute.return_value.scalars.return_value.first.return_value = None
    
    from datetime import date
    result, error = await set_item_due_date(mock_db, 999, date(2026, 3, 15), "user-123")
    
    assert result is None
    assert error == "not_found"


@pytest.mark.asyncio
async def test_set_item_due_date_no_permission(mock_db, mock_current_user):
    """Test set due date returns forbidden when user doesn't have permission."""
    from app.services.item_service import set_item_due_date
    
    # Mock item
    mock_item = MagicMock()
    mock_item.id = 1
    mock_item.list_id = 1
    
    # Mock list owned by different user
    mock_list_other = MagicMock()
    mock_list_other.id = 1
    mock_list_other.owner_id = "different-user"
    
    # Configure mock
    mock_db.execute.return_value.scalars.return_value.first.side_effect = [mock_item, mock_list_other]
    
    from datetime import date
    result, error = await set_item_due_date(mock_db, 1, date(2026, 3, 15), "user-123")
    
    assert result is None
    assert error == "forbidden"


@pytest.mark.asyncio
async def test_set_item_priority_success(mock_db, mock_current_user, mock_list):
    """Test successful setting of item priority."""
    from app.services.item_service import set_item_priority
    from app.models.todo_item import Priority
    
    # Mock item
    mock_item = MagicMock()
    mock_item.id = 1
    mock_item.list_id = 1
    mock_item.text = "Test task"
    mock_item.status = "not_started"
    mock_item.priority = None
    
    # Configure mock
    mock_db.execute.return_value.scalars.return_value.first.side_effect = [mock_item, mock_list]
    mock_db.commit = AsyncMock()
    mock_db.refresh = AsyncMock()
    mock_db.add = MagicMock()
    
    result, error = await set_item_priority(mock_db, 1, Priority.HIGH, "user-123")
    
    # Verify priority was set
    assert result is not None
    assert error is None
    assert result.priority == Priority.HIGH
    mock_db.commit.assert_called_once()


@pytest.mark.asyncio
async def test_set_item_priority_clear(mock_db, mock_current_user, mock_list):
    """Test clearing item priority."""
    from app.services.item_service import set_item_priority
    from app.models.todo_item import Priority
    
    # Mock item with existing priority
    mock_item = MagicMock()
    mock_item.id = 1
    mock_item.list_id = 1
    mock_item.text = "Test task"
    mock_item.status = "not_started"
    mock_item.priority = Priority.HIGH
    
    # Configure mock
    mock_db.execute.return_value.scalars.return_value.first.side_effect = [mock_item, mock_list]
    mock_db.commit = AsyncMock()
    mock_db.refresh = AsyncMock()
    mock_db.add = MagicMock()
    
    result, error = await set_item_priority(mock_db, 1, None, "user-123")
    
    # Verify priority was cleared
    assert result is not None
    assert error is None
    assert result.priority is None
    mock_db.commit.assert_called_once()


@pytest.mark.asyncio
async def test_set_item_priority_not_found(mock_db, mock_current_user):
    """Test set priority returns not_found when item doesn't exist."""
    from app.services.item_service import set_item_priority
    from app.models.todo_item import Priority
    
    # Configure mock to return None
    mock_db.execute.return_value.scalars.return_value.first.return_value = None
    
    result, error = await set_item_priority(mock_db, 999, Priority.HIGH, "user-123")
    
    assert result is None
    assert error == "not_found"


@pytest.mark.asyncio
async def test_set_item_priority_no_permission(mock_db, mock_current_user):
    """Test set priority returns forbidden when user doesn't have permission."""
    from app.services.item_service import set_item_priority
    from app.models.todo_item import Priority
    
    # Mock item
    mock_item = MagicMock()
    mock_item.id = 1
    mock_item.list_id = 1
    
    # Mock list owned by different user
    mock_list_other = MagicMock()
    mock_list_other.id = 1
    mock_list_other.owner_id = "different-user"
    
    # Configure mock
    mock_db.execute.return_value.scalars.return_value.first.side_effect = [mock_item, mock_list_other]
    
    result, error = await set_item_priority(mock_db, 1, Priority.HIGH, "user-123")
    
    assert result is None
    assert error == "forbidden"


@pytest.mark.asyncio
async def test_set_item_priority_all_levels(mock_db, mock_current_user, mock_list):
    """Test setting all priority levels (low, medium, high)."""
    from app.services.item_service import set_item_priority
    from app.models.todo_item import Priority
    
    # Test each priority level
    for priority in [Priority.LOW, Priority.MEDIUM, Priority.HIGH]:
        # Mock item
        mock_item = MagicMock()
        mock_item.id = 1
        mock_item.list_id = 1
        mock_item.text = "Test task"
        mock_item.status = "not_started"
        mock_item.priority = None
        
        # Configure mock
        mock_db.execute.return_value.scalars.return_value.first.side_effect = [mock_item, mock_list]
        mock_db.commit = AsyncMock()
        mock_db.refresh = AsyncMock()
        mock_db.add = MagicMock()
        
        result, error = await set_item_priority(mock_db, 1, priority, "user-123")
        
        assert result is not None
        assert error is None
        assert result.priority == priority
