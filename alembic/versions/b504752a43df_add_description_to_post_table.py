"""add description to post table

Revision ID: b504752a43df
Revises: 55f420870b80
Create Date: 2025-06-16 18:35:20.536453

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b504752a43df'
down_revision: Union[str, None] = '55f420870b80'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('posts', sa.Column('description', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'description')

    pass
