"""Remove is_completed, update status values

Revision ID: 20260220_remove_is_completed
Revises: xxxx_add_desc_tags_status
Create Date: 2026-02-20

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '20260220_remove_is_completed'
down_revision = 'xxxx_add_desc_tags_status'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # First, expand the status column to 50 chars (was 32)
    op.alter_column('todo_items', 'status', type_=sa.String(length=50), nullable=True)
    
    # Update existing status values from 'pending' to 'not_started'
    op.execute("UPDATE todo_items SET status = 'not_started' WHERE status = 'pending' OR status IS NULL")
    
    # Update status based on is_completed if needed
    op.execute("UPDATE todo_items SET status = 'completed' WHERE is_completed = true AND status != 'completed'")
    
    # Drop the index on is_completed
    op.drop_index('ix_todo_items_is_completed', table_name='todo_items')
    
    # Drop is_completed column
    op.drop_column('todo_items', 'is_completed')
    
    # Make status NOT NULL with default 'not_started' and add index
    op.alter_column('todo_items', 'status', nullable=False, server_default='not_started')
    op.create_index('ix_todo_items_status', 'todo_items', ['status'])


def downgrade() -> None:
    # Drop the status index
    op.drop_index('ix_todo_items_status', table_name='todo_items')
    
    # Revert status to nullable with 'pending' default
    op.alter_column('todo_items', 'status', nullable=True, server_default='pending')
    
    # Add is_completed column back
    op.add_column('todo_items', sa.Column('is_completed', sa.Boolean(), nullable=False, server_default='false'))
    
    # Add index on is_completed
    op.create_index('ix_todo_items_is_completed', 'todo_items', ['is_completed'])
    
    # Update status back to 'pending' for non-completed items
    op.execute("UPDATE todo_items SET status = 'pending' WHERE status = 'not_started'")
    op.execute("UPDATE todo_items SET status = 'completed' WHERE status = 'completed'")
    
    # Revert status column length back to 32
    op.alter_column('todo_items', 'status', type_=sa.String(length=32), nullable=True)
