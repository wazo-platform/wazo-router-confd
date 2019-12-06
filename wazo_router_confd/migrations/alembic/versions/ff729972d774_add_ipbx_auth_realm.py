"""add_ipbx_auth_realm

Revision ID: ff729972d774
Revises: 0d208181667d
Create Date: 2019-12-06 08:47:51.645414

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ff729972d774'
down_revision = '0d208181667d'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('ipbx', sa.Column('realm', sa.String(length=64), nullable=True))


def downgrade():
    op.drop_column('ipbx', 'realm')
