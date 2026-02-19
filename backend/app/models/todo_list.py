"""TodoList database model."""
from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional


class TodoList(SQLModel, table=True):
    """TodoList model for storing user TODO lists."""
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=255, index=True)
    owner_id: str = Field(index=True)  # References BetterAuth user.id (text)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
