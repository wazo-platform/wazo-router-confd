"""alter table tenants add column uuid

Revision ID: f21060542727
Revises: dcb824b74db0
Create Date: 2019-10-24 13:52:18.163490

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f21060542727'
down_revision = 'dcb824b74db0'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('tenants', sa.Column('uuid', sa.String(length=32), nullable=True))
    op.create_index(op.f('ix_tenants_uuid'), 'tenants', ['uuid'], unique=True)


def downgrade():
    op.drop_index(op.f('ix_tenants_uuid'), table_name='tenants')
    op.drop_column('tenants', 'uuid')
