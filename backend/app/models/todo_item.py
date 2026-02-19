"""TodoItem database model."""

from sqlmodel import SQLModel, Field
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


class TodoItem(SQLModel, table=True):
    """TodoItem model for storing TODO items within lists."""

    __tablename__ = "todo_items"

    id: Optional[int] = Field(default=None, primary_key=True)
    list_id: int = Field(foreign_key="todo_lists.id", index=True)
    text: str = Field(max_length=500)
    description: Optional[str] = Field(default=None, max_length=2000)
    tags: str = Field(default="[]")  # JSON array stored as string
    status: str = Field(
        default="not_started", max_length=50
    )  # not_started, in_progress, completed
    due_date: Optional[date] = Field(default=None, nullable=True)
    priority: Optional[Priority] = Field(default=None, nullable=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    deleted_at: Optional[datetime] = Field(
        default=None, nullable=True
    )  # Soft delete support
    created_by: str = Field(index=True)  # References BetterAuth user.id (text)

    def get_tags(self) -> List[str]:
        """Get tags as a list."""
        try:
            return json.loads(self.tags) if self.tags else []
        except json.JSONDecodeError:
            return []

    def set_tags(self, tags: List[str]):
        """Set tags from a list."""
        self.tags = json.dumps(tags)
