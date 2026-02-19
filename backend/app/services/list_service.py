"""TodoList service logic."""

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import SQLModel
from datetime import timezone, datetime

from app.models.todo_list import TodoList


async def create_list(db: AsyncSession, name: str, owner_id: str) -> TodoList:
    """
    Create a new TODO list.

    Args:
        db: Database session
        name: Name of the list
        owner_id: ID of the user creating the list

    Returns:
        Created TodoList object
    """
    new_list = TodoList(
        name=name,
        owner_id=owner_id,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )

    db.add(new_list)
    await db.commit()
    await db.refresh(new_list)

    return new_list


async def get_user_lists(db: AsyncSession, owner_id: str) -> list[TodoList]:
    """
    Get all lists for a specific user, ordered by most recently updated first.

    Args:
        db: Database session
        owner_id: ID of the user

    Returns:
        List of TodoList objects
    """
    result = await db.execute(
        select(TodoList)
        .where(TodoList.owner_id == owner_id)
        .order_by(TodoList.updated_at.desc())
    )
    return list(result.scalars().all())


async def get_list(db: AsyncSession, list_id: int, owner_id: str) -> TodoList | None:
    """
    Get a single list by ID, verifying ownership.

    Args:
        db: Database session
        list_id: ID of the list to retrieve
        owner_id: ID of the user (for ownership check)

    Returns:
        TodoList object if found and owned by user, None otherwise
    """
    result = await db.execute(
        select(TodoList).where(
            TodoList.id == list_id,
            TodoList.owner_id == owner_id
        )
    )
    return result.scalars().first()


async def update_list_name(
    db: AsyncSession, 
    list_id: int, 
    owner_id: str, 
    new_name: str
) -> TodoList | None:
    """
    Update a list's name, verifying ownership.

    Args:
        db: Database session
        list_id: ID of the list to update
        owner_id: ID of the user (for ownership check)
        new_name: New name for the list

    Returns:
        Updated TodoList object if found and owned by user, None otherwise
    """
    result = await db.execute(
        select(TodoList).where(
            TodoList.id == list_id,
            TodoList.owner_id == owner_id
        )
    )
    list_obj = result.scalars().first()
    
    if not list_obj:
        return None
    
    # Update name and timestamp
    list_obj.name = new_name
    list_obj.updated_at = datetime.now(timezone.utc)
    
    db.add(list_obj)
    await db.commit()
    await db.refresh(list_obj)
    return list_obj
