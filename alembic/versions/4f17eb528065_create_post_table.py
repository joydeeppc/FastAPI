"""create post table

Revision ID: 4f17eb528065
Revises: 
Create Date: 2024-02-24 21:25:38.927265

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4f17eb528065'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table('posts', sa.Column('id',sa.Integer(),nullable=False,primary_key=True), sa.Column('title', sa.String(),nullable=False))
    pass


# This fuction is for roleback. If I realized I messed it up, and I don't want it anymore, then we have to put in all of the logic in the downgrade function to handle removing the table.
def downgrade() -> None:
    pass
