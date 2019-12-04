"""Use tenant uuid instead of id for foreign keys

Revision ID: 464ce1bcefce
Revises: 84ca6bdd6c75
Create Date: 2019-12-04 07:44:50.111812

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy_utils import UUIDType


# revision identifiers, used by Alembic.
revision = '464ce1bcefce'
down_revision = '84ca6bdd6c75'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        'carriers', sa.Column('tenant_uuid', sa.UUIDType(), nullable=False)
    )
    op.create_foreign_key(
        None, 'carriers', 'tenants', ['tenant_uuid'], ['uuid'], ondelete='CASCADE'
    )
    op.create_unique_constraint("carriers", None, ["tenant_uuid", "id"])
    op.create_unique_constraint("carriers", None, ["tenant_uuid", "name"])
    op.create_foreign_key(
        None, 'carriers', 'tenants', ['tenant_uuid'], ['name'], ondelete='CASCADE'
    )


def downgrade():
    pass
