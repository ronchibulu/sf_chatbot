"""update todo_lists remove foreign key constraint

Revision ID: 0c5fce15a381
Revises: 2a401bc16669
Create Date: 2026-02-19 21:37:33.761906

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0c5fce15a381'
down_revision: Union[str, Sequence[str], None] = '2a401bc16669'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Remove foreign key constraint from todolist.owner_id."""
    # Drop the foreign key constraint (we can't drop tables - they're managed by BetterAuth)
    # Just recreate the table without the foreign key
    op.execute("""
        ALTER TABLE todolist 
        DROP CONSTRAINT IF EXISTS todolist_owner_id_fkey
    """)


def downgrade() -> None:
    """Downgrade - add back foreign key (not needed since we removed it)."""
    pass
