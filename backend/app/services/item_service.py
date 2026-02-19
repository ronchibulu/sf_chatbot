"""TodoItem service logic."""

import logging
from typing import cast

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import SQLModel
from datetime import timezone, datetime, date
import json

from app.models.todo_item import TodoItem
from app.models.todo_list import TodoList

logger = logging.getLogger(__name__)

# Sentinel value to distinguish between "not provided" and "explicitly set to None"
UNSET = object()


async def create_item(
    db: AsyncSession,
    list_id: int,
    text: str,
    created_by: str,
    description: str | None = None,
    tags: list[str] | None = None,
    status: str = "not_started",
) -> TodoItem:
    """
    Create a new TODO item.

    Args:
        db: Database session
        list_id: ID of the list to add the item to
        text: Text of the TODO item
        created_by: ID of the user creating the item
        description: Optional description of the TODO item
        tags: Optional list of tags
        status: Status of the TODO item (default: "not_started")

    Returns:
        Created TodoItem object
    """

    try:
        new_item = TodoItem(
            list_id=list_id,
            text=text,
            description=description,
            tags=json.dumps(tags) if tags else "[]",
            status=status,
            created_by=created_by,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )

        db.add(new_item)
        await db.commit()
        await db.refresh(new_item)

        return new_item
    except Exception as e:
        await db.rollback()
        print(f"Error creating item: {e}")
        import traceback

        traceback.print_exc()
        raise


async def get_items_by_list(db: AsyncSession, list_id: int) -> list[TodoItem]:
    """
    Get all items for a specific list, ordered by creation date (oldest first).
    Excludes soft-deleted items.

    Args:
        db: Database session
        list_id: ID of the list

    Returns:
        List of TodoItem objects
    """
    from sqlalchemy import and_

    result = await db.execute(
        select(TodoItem)
        .where(and_(TodoItem.list_id == list_id, TodoItem.deleted_at.is_(None)))
        .order_by(TodoItem.created_at.asc())
    )
    return list(result.scalars().all())


async def get_item(db: AsyncSession, item_id: int) -> TodoItem | None:
    """
    Get a single item by ID.

    Args:
        db: Database session
        item_id: ID of the item to retrieve

    Returns:
        TodoItem object if found, None otherwise
    """
    result = await db.execute(select(TodoItem).where(TodoItem.id == item_id))
    return result.scalars().first()


async def update_item(
    db: AsyncSession,
    item_id: int,
    new_text: str,
    user_id: str,
    description=UNSET,
    tags=UNSET,
    status=UNSET,
    due_date=UNSET,
    priority=UNSET,
) -> TodoItem | None:
    """
    Update a TODO item's text.

    Args:
        db: Database session
        item_id: ID of the item to update
        new_text: New text for the item
        user_id: ID of the user making the update
        description: Optional description (use None to clear)
        tags: Optional tags (use None to clear)
        status: Optional status (use None to clear)
        due_date: Optional due date (use None to clear)
        priority: Optional priority (use None to clear)

    Returns:
        Updated TodoItem object if successful, None otherwise
    """
    # Get the item
    result = await db.execute(select(TodoItem).where(TodoItem.id == item_id))
    item = result.scalars().first()

    if not item:
        return None

    # Check if user has permission (owner only for now - Epic 4 will add sharing)
    list_result = await db.execute(select(TodoList).where(TodoList.id == item.list_id))
    todo_list = list_result.scalars().first()

    if not todo_list:
        return None

    if todo_list.owner_id != user_id:
        return None

    # Update the text and timestamp
    item.text = new_text
    logger.info(
        f"update_item_text called with: description={description}, tags={tags}, status={status}, due_date={due_date}, priority={priority}, UNSET={UNSET}"
    )
    logger.info(f"description is UNSET: {description is UNSET}")
    logger.info(f"due_date is UNSET: {due_date is UNSET}")
    logger.info(f"priority is UNSET: {priority is UNSET}")
    if description is not UNSET:
        item.description = description if description else None
    if tags is not UNSET:
        item.tags = json.dumps(tags) if tags else "[]"
    if status is not UNSET:
        item.status = status
    if due_date is not UNSET:
        logger.info(f"Setting due_date to: {due_date} (type: {type(due_date)})")
        item.due_date = due_date
    if priority is not UNSET:
        logger.info(f"Setting priority to: {priority} (type: {type(priority)})")
        item.priority = priority
    item.updated_at = datetime.now(timezone.utc)

    db.add(item)
    await db.commit()
    await db.refresh(item)

    return item


async def toggle_item_completion(
    db: AsyncSession, item_id: int, user_id: str
) -> tuple[TodoItem | None, str | None]:
    """
    Toggle a TODO item's completion status.

    Args:
        db: Database session
        item_id: ID of the item to toggle
        user_id: ID of the user making the update

    Returns:
        Tuple of (Updated TodoItem object if successful, None if error, error message or None)
    """
    # Get the item
    result = await db.execute(select(TodoItem).where(TodoItem.id == item_id))
    item = result.scalars().first()

    if not item:
        return None, "not_found"

    # Check if user has permission (owner only for now - Epic 4 will add sharing)
    list_result = await db.execute(select(TodoList).where(TodoList.id == item.list_id))
    todo_list = list_result.scalars().first()

    if not todo_list or todo_list.owner_id != user_id:
        return None, "forbidden"

    # Toggle completion status
    if item.status == "completed":
        item.status = "not_started"
    else:
        item.status = "completed"
    item.updated_at = datetime.now(timezone.utc)

    db.add(item)
    await db.commit()
    await db.refresh(item)

    return item, None


async def delete_item(
    db: AsyncSession, item_id: int, user_id: str
) -> tuple[bool, str | None]:
    """
    Delete a TODO item (soft delete for undo support).

    Args:
        db: Database session
        item_id: ID of the item to delete
        user_id: ID of the user making the request

    Returns:
        Tuple of (success: bool, error: str or None)
    """
    # Get the item
    result = await db.execute(select(TodoItem).where(TodoItem.id == item_id))
    item = result.scalars().first()

    if not item:
        return False, "not_found"

    # Check if user has permission (owner only for now - Epic 4 will add sharing)
    list_result = await db.execute(select(TodoList).where(TodoList.id == item.list_id))
    todo_list = list_result.scalars().first()

    if not todo_list or todo_list.owner_id != user_id:
        return False, "forbidden"

    # Soft delete: mark as deleted and store deleted_at timestamp
    item.deleted_at = datetime.now(timezone.utc)

    db.add(item)
    await db.commit()

    return True, None


async def restore_item(
    db: AsyncSession, item_id: int, user_id: str
) -> tuple[TodoItem | None, str | None]:
    """
    Restore a recently deleted TODO item.

    Args:
        db: Database session
        item_id: ID of the item to restore
        user_id: ID of the user making the request

    Returns:
        Tuple of (Restored TodoItem object if successful, None if error, error message or None)
    """
    # Get the item
    result = await db.execute(select(TodoItem).where(TodoItem.id == item_id))
    item = result.scalars().first()

    if not item:
        return None, "not_found"

    # Check if user has permission (owner only for now - Epic 4 will add sharing)
    list_result = await db.execute(select(TodoList).where(TodoList.id == item.list_id))
    todo_list = list_result.scalars().first()

    if not todo_list or todo_list.owner_id != user_id:
        return None, "forbidden"

    # Check if item was actually deleted (has deleted_at timestamp within 5 seconds)
    if not item.deleted_at:
        return None, "not_deleted"

    # Check if deletion is still within the undo window (5 seconds)
    time_since_deletion = (datetime.now(timezone.utc) - item.deleted_at).total_seconds()
    if time_since_deletion > 5:
        return None, "undo_timeout"

    # Restore: clear the deleted_at timestamp
    item.deleted_at = None
    item.updated_at = datetime.now(timezone.utc)

    db.add(item)
    await db.commit()
    await db.refresh(item)

    return item, None


async def permanently_delete_item(db: AsyncSession, item_id: int) -> bool:
    """
    Permanently delete items that have been soft-deleted for more than 5 seconds.

    Args:
        db: Database session
        item_id: ID of the item to permanently delete

    Returns:
        True if deleted, False if not found
    """
    result = await db.execute(select(TodoItem).where(TodoItem.id == item_id))
    item = result.scalars().first()

    if not item:
        return False

    # Check if deletion window has passed (more than 5 seconds)
    if item.deleted_at:
        time_since_deletion = (
            datetime.now(timezone.utc) - item.deleted_at
        ).total_seconds()
        if time_since_deletion > 5:
            # Hard delete
            await db.delete(item)
            await db.commit()
            return True

    return False


async def set_item_due_date(
    db: AsyncSession, item_id: int, due_date, user_id: str
) -> tuple[TodoItem | None, str | None]:
    """
    Set or clear a TODO item's due date.

    Args:
        db: Database session
        item_id: ID of the item to update
        due_date: New due date (date object or None to clear)
        user_id: ID of the user making the request

    Returns:
        Tuple of (Updated TodoItem object if successful, None if error, error message or None)
    """
    # Get the item
    result = await db.execute(select(TodoItem).where(TodoItem.id == item_id))
    item = result.scalars().first()

    if not item:
        return None, "not_found"

    # Check if user has permission (owner only for now - Epic 4 will add sharing)
    list_result = await db.execute(select(TodoList).where(TodoList.id == item.list_id))
    todo_list = list_result.scalars().first()

    if not todo_list or todo_list.owner_id != user_id:
        return None, "forbidden"

    # Set or clear the due date
    item.due_date = due_date
    item.updated_at = datetime.now(timezone.utc)

    db.add(item)
    await db.commit()
    await db.refresh(item)

    return item, None


async def set_item_priority(
    db: AsyncSession, item_id: int, priority, user_id: str
) -> tuple[TodoItem | None, str | None]:
    """
    Set or clear a TODO item's priority.

    Args:
        db: Database session
        item_id: ID of the item to update
        priority: New priority (Priority enum or None to clear)
        user_id: ID of the user making the request

    Returns:
        Tuple of (Updated TodoItem object if successful, None if error, error message or None)
    """
    # Get the item
    result = await db.execute(select(TodoItem).where(TodoItem.id == item_id))
    item = result.scalars().first()

    if not item:
        return None, "not_found"

    # Check if user has permission (owner only for now - Epic 4 will add sharing)
    list_result = await db.execute(select(TodoList).where(TodoList.id == item.list_id))
    todo_list = list_result.scalars().first()

    if not todo_list or todo_list.owner_id != user_id:
        return None, "forbidden"

    # Set or clear the priority
    item.priority = priority
    item.updated_at = datetime.now(timezone.utc)

    db.add(item)
    await db.commit()
    await db.refresh(item)

    return item, None
