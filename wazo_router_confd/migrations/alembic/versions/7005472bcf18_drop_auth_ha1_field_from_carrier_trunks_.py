"""Drop auth_ha1 field from carrier_trunks table

Revision ID: 7005472bcf18
Revises: 053a622b66cb
Create Date: 2019-10-14 13:33:59.084344

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7005472bcf18'
down_revision = '053a622b66cb'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_column('ipbx', 'auth_ha1')


def downgrade():
    op.add_column(
        'ipbx',
        sa.Column(
            'auth_ha1', sa.VARCHAR(length=128), autoincrement=False, nullable=True
        ),
    )
