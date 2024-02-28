"""add content column to posts table

Revision ID: 3753ecbd69cc
Revises: 4f17eb528065
Create Date: 2024-02-25 20:28:30.212557

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3753ecbd69cc'
down_revision: Union[str, None] = '4f17eb528065'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('posts',sa.Column('content',sa.String(),nullable=False))
    pass


def downgrade():
    op.drop_column('posts','content')
    pass
