"""Create todo_items table

Revision ID: b2c3d4e5f6a7
Revises: a1b2c3d4e5f6
Create Date: 2026-02-19 23:30:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b2c3d4e5f6a7'
down_revision: Union[str, Sequence[str], None] = 'a1b2c3d4e5f6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create todo_items table."""
    op.create_table(
        'todo_items',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('list_id', sa.Integer(), nullable=False),
        sa.Column('text', sa.String(length=500), nullable=False),
        sa.Column('is_completed', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('created_by', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )
    
    # Add foreign key to todo_lists
    op.create_foreign_key(
        'fk_todo_items_list_id',
        'todo_items', 'todolist',
        ['list_id'], ['id'],
        ondelete='CASCADE'
    )
    
    # Add indexes for common queries
    op.create_index('ix_todo_items_list_id', 'todo_items', ['list_id'])
    op.create_index('ix_todo_items_is_completed', 'todo_items', ['is_completed'])
    op.create_index('ix_todo_items_created_by', 'todo_items', ['created_by'])


def downgrade() -> None:
    """Drop todo_items table."""
    op.drop_index('ix_todo_items_created_by', table_name='todo_items')
    op.drop_index('ix_todo_items_is_completed', table_name='todo_items')
    op.drop_index('ix_todo_items_list_id', table_name='todo_items')
    op.drop_constraint('fk_todo_items_list_id', 'todo_items', type_='foreignkey')
    op.drop_table('todo_items')
