"""normalization

Revision ID: dcb824b74db0
Revises: 7b3936f7f852
Create Date: 2019-10-21 21:26:32.492982

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dcb824b74db0'
down_revision = '7b3936f7f852'
branch_labels = None
depends_on = None


def upgrade():
    op.create_unique_constraint(None, 'carriers', ['tenant_id', 'id'])
    op.create_table(
        'normalization_profiles',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('tenant_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=256), nullable=False),
        sa.Column('country_code', sa.String(length=64), nullable=True),
        sa.Column('area_code', sa.String(length=64), nullable=True),
        sa.Column('intl_prefix', sa.String(length=64), nullable=True),
        sa.Column('ld_prefix', sa.String(length=64), nullable=True),
        sa.Column('always_intl_prefix_plus', sa.Boolean(), nullable=False),
        sa.Column('always_ld', sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(['tenant_id'], ['tenants.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name'),
        sa.UniqueConstraint('tenant_id', 'id'),
    )
    op.create_index(
        op.f('ix_normalization_profiles_id'),
        'normalization_profiles',
        ['id'],
        unique=False,
    )
    op.create_table(
        'normalization_rules',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('profile_id', sa.Integer(), nullable=False),
        sa.Column('rule_type', sa.Integer(), nullable=False),
        sa.Column('priority', sa.Integer(), nullable=False),
        sa.Column('match_regex', sa.String(length=256), nullable=False),
        sa.Column('match_prefix', sa.String(length=256), nullable=False),
        sa.Column('replace_regex', sa.String(length=256), nullable=False),
        sa.ForeignKeyConstraint(
            ['profile_id'], ['normalization_profiles.id'], ondelete='CASCADE'
        ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('profile_id', 'match_regex'),
    )
    op.create_index(
        op.f('ix_normalization_rules_id'), 'normalization_rules', ['id'], unique=False
    )
    op.add_column(
        'carrier_trunks',
        sa.Column('normalization_profile_id', sa.Integer(), nullable=True),
    )
    op.add_column(
        'carrier_trunks', sa.Column('tenant_id', sa.Integer(), nullable=False)
    )
    op.drop_index('ix_carrier_trunks_carrier_id', table_name='carrier_trunks')
    op.drop_constraint(
        'carrier_trunks_carrier_id_fkey', 'carrier_trunks', type_='foreignkey'
    )
    op.create_foreign_key(
        None, 'carrier_trunks', 'tenants', ['tenant_id'], ['id'], ondelete='CASCADE'
    )
    op.create_foreign_key(
        None,
        'carrier_trunks',
        'normalization_profiles',
        ['tenant_id', 'normalization_profile_id'],
        ['tenant_id', 'id'],
        ondelete='SET NULL',
    )
    op.create_foreign_key(
        None,
        'carrier_trunks',
        'carriers',
        ['tenant_id', 'carrier_id'],
        ['tenant_id', 'id'],
        ondelete='CASCADE',
    )
    op.add_column(
        'ipbx', sa.Column('normalization_profile_id', sa.Integer(), nullable=True)
    )
    op.create_foreign_key(
        None,
        'ipbx',
        'normalization_profiles',
        ['tenant_id', 'normalization_profile_id'],
        ['tenant_id', 'id'],
        ondelete='SET NULL',
    )


def downgrade():
    op.drop_constraint(None, 'ipbx', type_='foreignkey')
    op.drop_column('ipbx', 'normalization_profile_id')
    op.drop_constraint(None, 'carriers', type_='unique')
    op.drop_constraint(None, 'carrier_trunks', type_='foreignkey')
    op.drop_constraint(None, 'carrier_trunks', type_='foreignkey')
    op.drop_constraint(None, 'carrier_trunks', type_='foreignkey')
    op.create_foreign_key(
        'carrier_trunks_carrier_id_fkey',
        'carrier_trunks',
        'carriers',
        ['carrier_id'],
        ['id'],
        ondelete='CASCADE',
    )
    op.create_index(
        'ix_carrier_trunks_carrier_id', 'carrier_trunks', ['carrier_id'], unique=False
    )
    op.drop_column('carrier_trunks', 'tenant_id')
    op.drop_column('carrier_trunks', 'normalization_profile_id')
    op.drop_index(op.f('ix_normalization_rules_id'), table_name='normalization_rules')
    op.drop_table('normalization_rules')
    op.drop_index(
        op.f('ix_normalization_profiles_id'), table_name='normalization_profiles'
    )
    op.drop_table('normalization_profiles')
