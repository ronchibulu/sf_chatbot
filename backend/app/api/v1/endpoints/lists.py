"""TodoList API endpoints."""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import CurrentUser
from app.db.database import get_db
from app.schemas.todo_list import TodoListCreate, TodoListResponse
from app.services.list_service import create_list, get_user_lists, get_list, update_list_name


router = APIRouter(prefix="/lists", tags=["lists"])


class UpdateListNameRequest(BaseModel):
    """Schema for updating list name."""
    name: str = Field(..., min_length=1, max_length=255, description="New name for the list")


@router.post("", response_model=TodoListResponse, status_code=201)
async def create_todo_list(
    list_data: TodoListCreate,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    """
    Create a new TODO list.

    Requires authentication. List will be owned by the authenticated user.
    """
    new_list = await create_list(db, list_data.name, current_user["id"])
    return new_list


@router.get("", response_model=list[TodoListResponse])
async def get_lists(current_user: CurrentUser, db: AsyncSession = Depends(get_db)):
    """
    Get all TODO lists for the authenticated user.
    """
    lists = await get_user_lists(db, current_user["id"])
    return lists


@router.get("/{list_id}", response_model=TodoListResponse)
async def get_list_detail(
    list_id: int,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    """
    Get a specific TODO list by ID.

    Requires authentication.
    Returns 404 if list not found.
    Returns 403 if user doesn't have access to the list.
    """
    list_obj = await get_list(db, list_id, current_user["id"])
    
    if list_obj is None:
        # First check if list exists at all (might be 404 or 403)
        from sqlalchemy import select
        from app.models.todo_list import TodoList
        result = await db.execute(select(TodoList).where(TodoList.id == list_id))
        existing_list = result.scalars().first()
        
        if existing_list is None:
            raise HTTPException(status_code=404, detail="List not found")
        else:
            # List exists but user doesn't own it
            raise HTTPException(status_code=403, detail="You don't have access to this list")
    
    return list_obj


@router.put("/{list_id}/name", response_model=TodoListResponse)
async def update_todo_list_name(
    list_id: int,
    name_data: UpdateListNameRequest,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    """
    Update the name of a TODO list.

    Requires authentication.
    Returns 404 if list not found.
    Returns 403 if user doesn't own the list.
    """
    # First check if list exists
    from sqlalchemy import select
    from app.models.todo_list import TodoList
    result = await db.execute(select(TodoList).where(TodoList.id == list_id))
    existing_list = result.scalars().first()
    
    if existing_list is None:
        raise HTTPException(status_code=404, detail="List not found")
    
    # Check ownership
    if existing_list.owner_id != current_user["id"]:
        raise HTTPException(status_code=403, detail="You don't have access to this list")
    
    # Update the name
    list_obj = await update_list_name(db, list_id, current_user["id"], name_data.name)
    return list_obj
