"""add recurring fields to sessions

Revision ID: abcd1234efgh
Revises: 
Create Date: 2025-08-16

"""
from alembic import op
import sqlalchemy as sa

revision = 'abcd1234efgh'
down_revision = '6646b5f6fb56'
branch_labels = None
depends_on = None

def upgrade():
    op.add_column('sessions', sa.Column('is_recurring', sa.Boolean(), nullable=False, server_default=sa.text('0')))
    op.add_column('sessions', sa.Column('recur_group_id', sa.String(length=36), nullable=True))
    op.add_column('sessions', sa.Column('notes', sa.String(length=255), nullable=True))

def downgrade():
    op.drop_column('sessions', 'notes')
    op.drop_column('sessions', 'recur_group_id')
    op.drop_column('sessions', 'is_recurring')
