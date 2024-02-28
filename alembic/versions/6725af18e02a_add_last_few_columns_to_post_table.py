"""add last few columns to post table

Revision ID: 6725af18e02a
Revises: b26dedaba900
Create Date: 2024-02-26 01:19:26.816197

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6725af18e02a'
down_revision: Union[str, None] = 'b26dedaba900'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('posts',sa.Column('published', sa.Boolean(),nullable=False, server_default="TRUE"))
    op.add_column("posts",sa.Column('created_at', sa.TIMESTAMP(timezone=True),nullable=False,server_default=sa.text('NOW()')),)
    pass    


def downgrade():
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
