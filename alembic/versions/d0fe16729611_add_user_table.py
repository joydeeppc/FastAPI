"""add user table

Revision ID: d0fe16729611
Revises: 3753ecbd69cc
Create Date: 2024-02-25 20:40:10.394496

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd0fe16729611'
down_revision: Union[str, None] = '3753ecbd69cc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table('users', sa.Column('id',sa.Integer(),nullable=False),
                    sa.Column('email',sa.String(),nullable=False),
                    sa.Column('password',sa.String(),nullable=False),
                    sa.Column('created_at',sa.TIMESTAMP(timezone=True),server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email') )
    pass


def downgrade():
    op.drop_table('users')
    pass
