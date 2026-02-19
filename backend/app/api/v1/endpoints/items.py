"""TodoItem API endpoints."""

import logging
from fastapi import APIRouter, Depends, HTTPException, status, Request
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.item_service import UNSET, get_item
from sqlalchemy import select

from app.api.deps import CurrentUser, get_db
from app.schemas.todo_item import TodoItemCreate, TodoItemResponse
from app.services.item_service import (
    create_item,
    get_items_by_list,
    update_item,
    toggle_item_completion,
    delete_item,
    restore_item,
    permanently_delete_item,
    set_item_due_date,
    set_item_priority,
)
from app.models.todo_list import TodoList
from app.models.todo_item import Priority
from pydantic import BaseModel
from typing import Optional, List
from datetime import date

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/lists/{list_id}/items", tags=["items"])
items_router = APIRouter(prefix="/items", tags=["items"])


class UpdateItemTextRequest(BaseModel):
    """Schema for updating item text."""

    text: str = Field(
        ..., min_length=1, max_length=500, description="New text for the item"
    )
    description: str | None = None
    tags: list[str] | None = None
    status: str | None = None
    due_date: date | None = None
    priority: str | None = None


@router.get("", response_model=List[TodoItemResponse])
async def get_items(
    list_id: int,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    """
    Get all TODO items for a specific list.

    Requires authentication. User must have access to the list.
    Returns 404 if list not found.
    Returns 403 if user doesn't have access to the list.
    """
    # Check if list exists and user has access
    logger.info(f"Getting items from list {list_id} for user {current_user['id']}")

    try:
        result = await db.execute(select(TodoList).where(TodoList.id == list_id))
        list_obj = result.scalars().first()

        if list_obj is None:
            raise HTTPException(status_code=404, detail="List not found")

        # Check if user has access (owner only for now - Epic 4 will add sharing)
        if list_obj.owner_id != current_user["id"]:
            raise HTTPException(
                status_code=403, detail="You don't have access to this list"
            )

        # Get items for the list
        items = await get_items_by_list(db, list_id)
        return items
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting items: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.post("", response_model=TodoItemResponse, status_code=status.HTTP_201_CREATED)
async def create_todo_item(
    list_id: int,
    item_data: TodoItemCreate,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    """
    Create a new TODO item in a list.

    Requires authentication. User must have access to the list.
    Returns 404 if list not found.
    Returns 403 if user doesn't have access to the list.
    """
    # Check if list exists and user has access
    logger.info(f"Creating item in list {list_id} for user {current_user['id']}")

    try:
        result = await db.execute(select(TodoList).where(TodoList.id == list_id))
        list_obj = result.scalars().first()

        if list_obj is None:
            raise HTTPException(status_code=404, detail="List not found")

        # Check if user has access (owner only for now - Epic 4 will add sharing)
        if list_obj.owner_id != current_user["id"]:
            raise HTTPException(
                status_code=403, detail="You don't have access to this list"
            )

        # Create the item
        new_item = await create_item(
            db,
            list_id,
            item_data.text,
            current_user["id"],
            description=item_data.description,
            tags=item_data.tags,
            status=item_data.status,
        )
        return new_item
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating item: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.put("/{item_id}", response_model=TodoItemResponse)
async def update_todo_item(
    list_id: int,
    item_id: int,
    text_data: UpdateItemTextRequest,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
    request: Request = None,  # type: ignore[assignment]
):
    """
    Update a TODO item in a list.

    Requires authentication. User must have access to the list.
    Returns 404 if list or item not found.
    Returns 403 if user doesn't have access to the list.
    """
    logger.info(
        f"Updating item {item_id} in list {list_id} by user {current_user['id']}"
    )

    try:
        # Check if list exists and user has access
        result = await db.execute(select(TodoList).where(TodoList.id == list_id))
        list_obj = result.scalars().first()

        if list_obj is None:
            raise HTTPException(status_code=404, detail="List not found")

        # Check if user has access (owner only for now)
        if list_obj.owner_id != current_user["id"]:
            raise HTTPException(
                status_code=403, detail="You don't have access to this list"
            )

        item = await get_item(db, item_id)

        if item is None:
            raise HTTPException(status_code=404, detail="Item not found")

        # Verify item belongs to this list
        if item.list_id != list_id:
            raise HTTPException(status_code=404, detail="Item not found in this list")

        # Parse the request body directly to see what fields were sent
        body = await request.json()
        logger.info(f"Request body: {body}")

        print("body", body)

        # Only update fields that were explicitly provided in the request
        provided_fields = {}
        for field_name in ["description", "tags", "status", "due_date", "priority"]:
            if field_name in body:
                provided_fields[field_name] = body[field_name]

        print(provided_fields)

        logger.info(f"Provided fields: {provided_fields}")

        updated_item = await update_item(
            db,
            item_id,
            text_data.text,
            current_user["id"],
            description=provided_fields.get("description", UNSET),
            tags=provided_fields.get("tags", UNSET),
            status=provided_fields.get("status", UNSET),
            due_date=provided_fields.get("due_date", UNSET),
            priority=provided_fields.get("priority", UNSET),
        )

        if updated_item is None:
            raise HTTPException(status_code=500, detail="Failed to update item")

        return updated_item
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating item: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@items_router.put("/{item_id}", response_model=TodoItemResponse)
async def update_todo_item_text(
    item_id: int,
    text_data: UpdateItemTextRequest,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
    request: Request = None,  # type: ignore[assignment]
):
    """
    Update a TODO item's text.

    Requires authentication. User must have permission to edit the item.
    Returns 404 if item not found.
    Returns 403 if user doesn't have permission to edit the item.
    """
    logger.info(f"Updating item {item_id} by user {current_user.get('id')}")

    print("updating in item-router")

    # Parse the request body directly to see what fields were sent
    body = await request.json()
    logger.info(f"Request body: {body}")

    # Only update fields that were explicitly provided in the request
    provided_fields = {}
    for field_name in ["description", "tags", "status", "due_date", "priority"]:
        if field_name in body:
            provided_fields[field_name] = body[field_name]

    logger.info(f"Provided fields: {provided_fields}")

    updated_item = await update_item(
        db,
        item_id,
        text_data.text,
        current_user["id"],
        description=provided_fields.get("description", UNSET),
        tags=provided_fields.get("tags", UNSET),
        status=provided_fields.get("status", UNSET),
        due_date=provided_fields.get("due_date", UNSET),
        priority=provided_fields.get("priority", UNSET),
    )

    if updated_item is None:
        item = await get_item(db, item_id)
        if item is None:
            logger.warning(f"Item {item_id} not found")
            raise HTTPException(status_code=404, detail="Item not found")
        else:
            # Check the list to see why permission failed
            list_result = await db.execute(
                select(TodoList).where(TodoList.id == item.list_id)
            )
            todo_list = list_result.scalars().first()
            logger.warning(
                f"Permission denied: user={current_user.get('id')}, list_owner={todo_list.owner_id if todo_list else 'list not found'}"
            )
            raise HTTPException(
                status_code=403, detail="You don't have permission to edit this item"
            )

    return updated_item


@items_router.patch("/{item_id}/toggle-complete", response_model=TodoItemResponse)
async def toggle_todo_item_completion(
    item_id: int,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    """
    Toggle a TODO item's completion status.

    Requires authentication. User must have permission to edit the item (Owner/Editor only).
    Returns 404 if item not found.
    Returns 403 if user doesn't have permission to edit the item.
    """
    # Toggle the item completion
    updated_item, error = await toggle_item_completion(db, item_id, current_user["id"])

    if error == "not_found":
        raise HTTPException(status_code=404, detail="Item not found")
    elif error == "forbidden":
        raise HTTPException(
            status_code=403, detail="You don't have permission to complete this item"
        )
    elif updated_item is None:
        raise HTTPException(status_code=500, detail="Failed to toggle item completion")

    return updated_item


@items_router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo_item(
    item_id: int,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    """
    Delete a TODO item (soft delete for undo support).

    Requires authentication. User must have permission to delete the item (Owner/Editor only).
    Returns 204 on success.
    Returns 404 if item not found.
    Returns 403 if user doesn't have permission to delete the item.
    """
    success, error = await delete_item(db, item_id, current_user["id"])

    if error == "not_found":
        raise HTTPException(status_code=404, detail="Item not found")
    elif error == "forbidden":
        raise HTTPException(
            status_code=403, detail="You don't have permission to delete this item"
        )

    return None


@items_router.post("/{item_id}/restore", response_model=TodoItemResponse)
async def restore_todo_item(
    item_id: int,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    """
    Restore a recently deleted TODO item.

    Requires authentication. User must have permission to restore the item.
    Returns 200 with restored item on success.
    Returns 404 if item not found, not deleted, or undo timeout expired.
    Returns 403 if user doesn't have permission to restore the item.
    """
    restored_item, error = await restore_item(db, item_id, current_user["id"])

    if error == "not_found":
        raise HTTPException(
            status_code=404, detail="Item not found or cannot be restored"
        )
    elif error == "not_deleted":
        raise HTTPException(status_code=404, detail="Item was not deleted")
    elif error == "undo_timeout":
        raise HTTPException(
            status_code=410, detail="Undo timeout expired - item cannot be restored"
        )
    elif error == "forbidden":
        raise HTTPException(
            status_code=403, detail="You don't have permission to restore this item"
        )
    elif restored_item is None:
        raise HTTPException(status_code=500, detail="Failed to restore item")

    return restored_item


class SetDueDateRequest(BaseModel):
    """Schema for setting item due date."""

    due_date: Optional[date] = None


class SetPriorityRequest(BaseModel):
    """Schema for setting item priority."""

    priority: Optional[str] = None


@items_router.patch("/{item_id}/due-date", response_model=TodoItemResponse)
async def set_due_date(
    item_id: int,
    data: SetDueDateRequest,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    """
    Set or clear a TODO item's due date.

    Requires authentication. User must have permission to edit the item.
    Returns 200 with updated item on success.
    Returns 404 if item not found.
    Returns 403 if user doesn't have permission.
    """
    updated_item, error = await set_item_due_date(
        db, item_id, data.due_date, current_user["id"]
    )

    if error == "not_found":
        raise HTTPException(status_code=404, detail="Item not found")
    elif error == "forbidden":
        raise HTTPException(
            status_code=403, detail="You don't have permission to edit this item"
        )
    elif updated_item is None:
        raise HTTPException(status_code=500, detail="Failed to update due date")

    return updated_item


@items_router.patch("/{item_id}/priority", response_model=TodoItemResponse)
async def set_priority(
    item_id: int,
    data: SetPriorityRequest,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    """
    Set or clear a TODO item's priority.

    Requires authentication. User must have permission to edit the item.
    Returns 200 with updated item on success.
    Returns 404 if item not found.
    Returns 403 if user doesn't have permission.
    """
    # Convert string priority to enum if provided
    priority_value = None
    if data.priority and data.priority in ["low", "medium", "high"]:
        priority_value = Priority[data.priority.upper()]

    updated_item, error = await set_item_priority(
        db, item_id, priority_value, current_user["id"]
    )

    if error == "not_found":
        raise HTTPException(status_code=404, detail="Item not found")
    elif error == "forbidden":
        raise HTTPException(
            status_code=403, detail="You don't have permission to edit this item"
        )
    elif updated_item is None:
        raise HTTPException(status_code=500, detail="Failed to update priority")

    return updated_item
