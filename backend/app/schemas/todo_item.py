"""TodoItem Pydantic schemas."""
from pydantic import BaseModel, Field, field_validator
from datetime import datetime, date
from typing import Optional, List
import json
from enum import Enum


class Priority(str, Enum):
    """Priority levels for TODO items."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class TodoItemStatus(str, Enum):
    """Status levels for TODO items."""
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class TodoItemCreate(BaseModel):
    """Schema for creating a TODO item."""
    text: str = Field(..., min_length=1, max_length=500, description="Text of the TODO item")
    description: Optional[str] = Field(None, max_length=2000, description="Detailed description of the TODO item")
    tags: List[str] = Field(default_factory=list, description="Tags associated with the TODO item")
    status: str = Field(default="not_started", description="Status of the TODO item: not_started, in_progress, completed")
    due_date: Optional[date] = Field(None, description="Due date for the TODO item")
    priority: Optional[Priority] = Field(None, description="Priority of the TODO item: low, medium, high")


class TodoItemResponse(BaseModel):
    """Schema for TODO item response."""
    id: int
    list_id: int
    text: str
    description: Optional[str] = None
    tags: List[str] = []
    status: str = "not_started"
    due_date: Optional[date] = None
    priority: Optional[Priority] = None
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None
    created_by: str
    
    class Config:
        from_attributes = True
    
    @field_validator('tags', mode='before')
    @classmethod
    def parse_tags(cls, v):
        if isinstance(v, str):
            try:
                return json.loads(v) if v else []
            except json.JSONDecodeError:
                return []
        return v if isinstance(v, list) else []
