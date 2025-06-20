"""add foreign key to post table

Revision ID: 67f6bf63e192
Revises: 8dc656f448d5
Create Date: 2025-06-16 18:40:01.114036

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '67f6bf63e192'
down_revision: Union[str, None] = '8dc656f448d5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fk', source_table="posts", referent_table="users", local_cols=[
                          'owner_id'], remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade() -> None:
    
    op.drop_constraint('post_users_fk', table_name="posts")
    op.drop_column('posts', 'owner_id')    
    pass

