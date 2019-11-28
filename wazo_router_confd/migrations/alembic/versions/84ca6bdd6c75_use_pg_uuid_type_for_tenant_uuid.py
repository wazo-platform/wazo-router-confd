"""Use pg uuid type for tenant uuid

Revision ID: 84ca6bdd6c75
Revises: f21060542727
Create Date: 2019-11-28 09:29:19.781527

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy_utils import UUIDType


# revision identifiers, used by Alembic.
revision = '84ca6bdd6c75'
down_revision = 'f21060542727'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column(
        "tenants", "uuid", nullable=False, type_=UUIDType,
        server_default='gen_random_uuid()',
    )
    op.alter_column(
        "tenants", "uuid", server_default=None,
    )


def downgrade():
    op.alter_column(
        "tenants", "uuid", nullable=True, type_=sa.String(32),
    )
