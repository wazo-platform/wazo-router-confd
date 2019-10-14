"""Add password field to ipbx table

Revision ID: 053a622b66cb
Revises: 7b3936f7f852
Create Date: 2019-10-14 13:17:13.949108

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '053a622b66cb'
down_revision = '7b3936f7f852'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_column('ipbx', 'sha1')
    op.drop_column('ipbx', 'sha1b')
    op.add_column(
        'ipbx',
        sa.Column(
            'password', sa.VARCHAR(length=192), autoincrement=False, nullable=True
        ),
    )


def downgrade():
    op.drop_column('ipbx', 'password')
    op.add_column(
        'ipbx',
        sa.Column('sha1', sa.VARCHAR(length=128), autoincrement=False, nullable=True),
    )
    op.add_column(
        'ipbx',
        sa.Column('sha1b', sa.VARCHAR(length=128), autoincrement=False, nullable=True),
    )
