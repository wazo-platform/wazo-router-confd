"""Add password_ha1 field to ipbx table

Revision ID: fc206a0c3ab1
Revises: 7005472bcf18
Create Date: 2019-10-15 17:44:19.841158

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fc206a0c3ab1'
down_revision = '7005472bcf18'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        'ipbx',
        sa.Column(
            'password_ha1', sa.VARCHAR(length=32), autoincrement=False, nullable=True
        ),
    )


def downgrade():
    op.drop_column('ipbx', 'password_ha1')
