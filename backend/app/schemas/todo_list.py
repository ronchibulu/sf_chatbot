"""TodoList Pydantic schemas."""
from pydantic import BaseModel, Field
from datetime import datetime


class TodoListCreate(BaseModel):
    """Schema for creating a TODO list."""
    name: str = Field(..., min_length=1, max_length=255, description="Name of the TODO list")


class TodoListResponse(BaseModel):
    """Schema for TODO list response."""
    id: int
    name: str
    owner_id: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
