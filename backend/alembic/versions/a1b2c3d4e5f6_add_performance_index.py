"""Add performance index for todo_lists

Revision ID: a1b2c3d4e5f6
Revises: 0c5fce15a381
Create Date: 2026-02-19 22:00:00.000000

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = 'a1b2c3d4e5f6'
down_revision: Union[str, Sequence[str], None] = '0c5fce15a381'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add composite index on owner_id and updated_at for performance."""
    op.execute("""
        CREATE INDEX IF NOT EXISTS idx_todo_lists_owner_updated 
        ON todolist (owner_id, updated_at DESC)
    """)


def downgrade() -> None:
    """Remove the performance index."""
    op.execute("DROP INDEX IF EXISTS idx_todo_lists_owner_updated")
