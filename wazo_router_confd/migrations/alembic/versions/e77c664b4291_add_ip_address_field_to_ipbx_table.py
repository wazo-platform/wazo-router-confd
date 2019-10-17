"""add_ip_address_field_to_ipbx_table

Revision ID: e77c664b4291
Revises: fc206a0c3ab1
Create Date: 2019-10-16 10:41:35.096202

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e77c664b4291'
down_revision = 'fc206a0c3ab1'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        'ipbx',
        sa.Column(
            'ip_address', sa.VARCHAR(length=256), autoincrement=False, nullable=True
        ),
    )


def downgrade():
    op.drop_column('ipbx', 'ip_address')
