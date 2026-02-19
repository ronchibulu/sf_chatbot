"""create todo_lists table

Revision ID: 2a401bc16669
Revises: 
Create Date: 2026-02-19 21:11:31.825508

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2a401bc16669'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create todo_lists table
    op.create_table(
        'todolist',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('owner_id', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['owner_id'], ['user.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_todolist_name'), 'todolist', ['name'], unique=False)
    op.create_index(op.f('ix_todolist_owner_id'), 'todolist', ['owner_id'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_todolist_owner_id'), table_name='todolist')
    op.drop_index(op.f('ix_todolist_name'), table_name='todolist')
    op.drop_table('todolist')
