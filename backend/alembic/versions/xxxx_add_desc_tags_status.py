"""Add description, tags, status to todo_items

Revision ID: xxxx_add_desc_tags_status
Revises: 
Create Date: 2026-02-20

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'xxxx_add_desc_tags_status'
down_revision = 'b2c3d4e5f6a7'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add description column
    op.add_column('todo_items', sa.Column('description', sa.String(length=2000), nullable=True))
    
    # Add tags column (stored as JSON string)
    op.add_column('todo_items', sa.Column('tags', sa.String(length=1000), nullable=True, server_default='[]'))
    
    # Add status column
    op.add_column('todo_items', sa.Column('status', sa.String(length=50), nullable=True, server_default='pending'))


def downgrade() -> None:
    op.drop_column('todo_items', 'status')
    op.drop_column('todo_items', 'tags')
    op.drop_column('todo_items', 'description')
