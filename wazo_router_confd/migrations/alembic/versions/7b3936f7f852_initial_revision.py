# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

"""Initial revision

Revision ID: 7b3936f7f852
Revises:
Create Date: 2019-10-01 09:41:26.886887

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '7b3936f7f852'
down_revision = None
branch_labels = None
depends_on = None


def downgrade():
    op.drop_index('ix_routing_groups_id', table_name='routing_groups')
    op.drop_table('routing_groups')
    op.drop_index('ix_domains_domain', table_name='domains')
    op.drop_index('ix_domains_id', table_name='domains')
    op.drop_table('domains')
    op.drop_index('ix_routing_rules_id', table_name='routing_rules')
    op.drop_table('routing_rules')
    op.drop_index('ix_tenants_id', table_name='tenants')
    op.drop_index('ix_tenants_name', table_name='tenants')
    op.drop_table('tenants')
    op.drop_index('ix_cdrs_id', table_name='cdrs')
    op.drop_table('cdrs')
    op.drop_index('ix_carrier_trunks_id', table_name='carrier_trunks')
    op.drop_index('ix_carrier_trunks_name', table_name='carrier_trunks')
    op.drop_table('carrier_trunks')
    op.drop_index('ix_dids_did_prefix', table_name='dids')
    op.drop_index('ix_dids_id', table_name='dids')
    op.drop_table('dids')
    op.drop_index('ix_ipbx_id', table_name='ipbx')
    op.drop_table('ipbx')
    op.drop_index('ix_carriers_id', table_name='carriers')
    op.drop_index('ix_carriers_name', table_name='carriers')
    op.drop_table('carriers')


def upgrade():
    op.create_table(
        'tenants',
        sa.Column(
            'id',
            sa.INTEGER(),
            server_default=sa.text("nextval('tenants_id_seq'::regclass)"),
            autoincrement=True,
            nullable=False,
        ),
        sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.PrimaryKeyConstraint('id', name='tenants_pkey'),
        postgresql_ignore_search_path=False,
    )
    op.create_index('ix_tenants_name', 'tenants', ['name'], unique=True)
    op.create_index('ix_tenants_id', 'tenants', ['id'], unique=False)
    #
    op.create_table(
        'domains',
        sa.Column(
            'id',
            sa.INTEGER(),
            server_default=sa.text("nextval('domains_id_seq'::regclass)"),
            autoincrement=True,
            nullable=False,
        ),
        sa.Column('domain', sa.VARCHAR(length=64), autoincrement=False, nullable=True),
        sa.Column('tenant_id', sa.INTEGER(), autoincrement=False, nullable=False),
        sa.ForeignKeyConstraint(
            ['tenant_id'],
            ['tenants.id'],
            name='domains_tenant_id_fkey',
            ondelete='CASCADE',
        ),
        sa.PrimaryKeyConstraint('id', name='domains_pkey'),
        sa.UniqueConstraint('tenant_id', 'id', name='domains_tenant_id_id_key'),
        postgresql_ignore_search_path=False,
    )
    op.create_index('ix_domains_id', 'domains', ['id'], unique=False)
    op.create_index('ix_domains_domain', 'domains', ['domain'], unique=True)
    #
    op.create_table(
        'carriers',
        sa.Column(
            'id',
            sa.INTEGER(),
            server_default=sa.text("nextval('carriers_id_seq'::regclass)"),
            autoincrement=True,
            nullable=False,
        ),
        sa.Column('tenant_id', sa.INTEGER(), autoincrement=False, nullable=False),
        sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.ForeignKeyConstraint(
            ['tenant_id'],
            ['tenants.id'],
            name='carriers_tenant_id_fkey',
            ondelete='CASCADE',
        ),
        sa.PrimaryKeyConstraint('id', name='carriers_pkey'),
        postgresql_ignore_search_path=False,
    )
    op.create_index('ix_carriers_name', 'carriers', ['name'], unique=True)
    op.create_index('ix_carriers_id', 'carriers', ['id'], unique=False)
    #
    op.create_table(
        'carrier_trunks',
        sa.Column(
            'id',
            sa.INTEGER(),
            server_default=sa.text("nextval('carrier_trunks_id_seq'::regclass)"),
            autoincrement=True,
            nullable=False,
        ),
        sa.Column('carrier_id', sa.INTEGER(), autoincrement=False, nullable=False),
        sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column('sip_proxy', sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.Column('sip_proxy_port', sa.INTEGER(), autoincrement=False, nullable=False),
        sa.Column('registered', sa.BOOLEAN(), autoincrement=False, nullable=True),
        sa.Column(
            'auth_username', sa.VARCHAR(length=35), autoincrement=False, nullable=True
        ),
        sa.Column(
            'auth_password', sa.VARCHAR(length=64), autoincrement=False, nullable=True
        ),
        sa.Column(
            'auth_ha1', sa.VARCHAR(length=128), autoincrement=False, nullable=True
        ),
        sa.Column('realm', sa.VARCHAR(length=64), autoincrement=False, nullable=True),
        sa.Column(
            'registrar_proxy',
            sa.VARCHAR(length=128),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column(
            'from_domain', sa.VARCHAR(length=64), autoincrement=False, nullable=True
        ),
        sa.Column('expire_seconds', sa.INTEGER(), autoincrement=False, nullable=False),
        sa.Column('retry_seconds', sa.INTEGER(), autoincrement=False, nullable=False),
        sa.ForeignKeyConstraint(
            ['carrier_id'],
            ['carriers.id'],
            name='carrier_trunks_carrier_id_fkey',
            ondelete='CASCADE',
        ),
        sa.PrimaryKeyConstraint('id', name='carrier_trunks_pkey'),
        postgresql_ignore_search_path=False,
    )
    op.create_index('ix_carrier_trunks_name', 'carrier_trunks', ['name'], unique=True)
    op.create_index('ix_carrier_trunks_id', 'carrier_trunks', ['id'], unique=False)
    #
    op.create_table(
        'ipbx',
        sa.Column(
            'id',
            sa.INTEGER(),
            server_default=sa.text("nextval('ipbx_id_seq'::regclass)"),
            autoincrement=True,
            nullable=False,
        ),
        sa.Column('tenant_id', sa.INTEGER(), autoincrement=False, nullable=False),
        sa.Column('domain_id', sa.INTEGER(), autoincrement=False, nullable=False),
        sa.Column('customer', sa.INTEGER(), autoincrement=False, nullable=True),
        sa.Column('ip_fqdn', sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.Column('port', sa.INTEGER(), autoincrement=False, nullable=False),
        sa.Column('registered', sa.BOOLEAN(), autoincrement=False, nullable=False),
        sa.Column(
            'username', sa.VARCHAR(length=50), autoincrement=False, nullable=True
        ),
        sa.Column('sha1', sa.VARCHAR(length=128), autoincrement=False, nullable=True),
        sa.Column('sha1b', sa.VARCHAR(length=128), autoincrement=False, nullable=True),
        sa.ForeignKeyConstraint(
            ['tenant_id', 'domain_id'],
            ['domains.tenant_id', 'domains.id'],
            name='ipbx_tenant_id_fkey',
            ondelete='CASCADE',
        ),
        sa.ForeignKeyConstraint(
            ['tenant_id'],
            ['tenants.id'],
            name='ipbx_tenant_id_fkey1',
            ondelete='CASCADE',
        ),
        sa.PrimaryKeyConstraint('id', name='ipbx_pkey'),
        sa.UniqueConstraint('tenant_id', 'id', name='ipbx_tenant_id_id_key'),
        postgresql_ignore_search_path=False,
    )
    op.create_index('ix_ipbx_id', 'ipbx', ['id'], unique=False)
    #
    op.create_table(
        'dids',
        sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column('tenant_id', sa.INTEGER(), autoincrement=False, nullable=False),
        sa.Column('ipbx_id', sa.INTEGER(), autoincrement=False, nullable=False),
        sa.Column(
            'carrier_trunk_id', sa.INTEGER(), autoincrement=False, nullable=False
        ),
        sa.Column('did_regex', sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column('did_prefix', sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.ForeignKeyConstraint(
            ['carrier_trunk_id'],
            ['carrier_trunks.id'],
            name='dids_carrier_trunk_id_fkey',
            ondelete='CASCADE',
        ),
        sa.ForeignKeyConstraint(
            ['tenant_id', 'ipbx_id'],
            ['ipbx.tenant_id', 'ipbx.id'],
            name='dids_tenant_id_fkey',
            ondelete='CASCADE',
        ),
        sa.ForeignKeyConstraint(
            ['tenant_id'],
            ['tenants.id'],
            name='dids_tenant_id_fkey1',
            ondelete='CASCADE',
        ),
        sa.PrimaryKeyConstraint('id', name='dids_pkey'),
        sa.UniqueConstraint('did_regex', name='dids_did_regex_key'),
    )
    op.create_index('ix_dids_id', 'dids', ['id'], unique=False)
    op.create_index('ix_dids_did_prefix', 'dids', ['did_prefix'], unique=False)
    #
    op.create_table(
        'cdrs',
        sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column('tenant_id', sa.INTEGER(), autoincrement=False, nullable=False),
        sa.Column('source_ip', sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.Column('source_port', sa.INTEGER(), autoincrement=False, nullable=False),
        sa.Column('from_uri', sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.Column('to_uri', sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.Column('call_id', sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.Column(
            'call_start', postgresql.TIMESTAMP(), autoincrement=False, nullable=True
        ),
        sa.Column('duration', sa.INTEGER(), autoincrement=False, nullable=True),
        sa.ForeignKeyConstraint(
            ['tenant_id'],
            ['tenants.id'],
            name='cdrs_tenant_id_fkey',
            ondelete='CASCADE',
        ),
        sa.PrimaryKeyConstraint('id', name='cdrs_pkey'),
    )
    op.create_index('ix_cdrs_id', 'cdrs', ['id'], unique=False)
    #
    op.create_table(
        'routing_rules',
        sa.Column(
            'id',
            sa.INTEGER(),
            server_default=sa.text("nextval('routing_rules_id_seq'::regclass)"),
            autoincrement=True,
            nullable=False,
        ),
        sa.Column('prefix', sa.VARCHAR(length=15), autoincrement=False, nullable=True),
        sa.Column(
            'carrier_trunk_id', sa.INTEGER(), autoincrement=False, nullable=False
        ),
        sa.Column('ipbx_id', sa.INTEGER(), autoincrement=False, nullable=False),
        sa.Column('did_regex', sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.Column(
            'route_type', sa.VARCHAR(length=10), autoincrement=False, nullable=False
        ),
        sa.ForeignKeyConstraint(
            ['carrier_trunk_id'],
            ['carrier_trunks.id'],
            name='routing_rules_carrier_trunk_id_fkey',
            ondelete='CASCADE',
        ),
        sa.ForeignKeyConstraint(
            ['ipbx_id'],
            ['ipbx.id'],
            name='routing_rules_ipbx_id_fkey',
            ondelete='CASCADE',
        ),
        sa.PrimaryKeyConstraint('id', name='routing_rules_pkey'),
        postgresql_ignore_search_path=False,
    )
    op.create_index('ix_routing_rules_id', 'routing_rules', ['id'], unique=False)
    #
    op.create_table(
        'routing_groups',
        sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column('tenant_id', sa.INTEGER(), autoincrement=False, nullable=False),
        sa.Column('routing_rule', sa.INTEGER(), autoincrement=False, nullable=True),
        sa.ForeignKeyConstraint(
            ['routing_rule'],
            ['routing_rules.id'],
            name='routing_groups_routing_rule_fkey',
            ondelete='CASCADE',
        ),
        sa.ForeignKeyConstraint(
            ['tenant_id'],
            ['tenants.id'],
            name='routing_groups_tenant_id_fkey',
            ondelete='CASCADE',
        ),
        sa.PrimaryKeyConstraint('id', name='routing_groups_pkey'),
    )
    op.create_index('ix_routing_groups_id', 'routing_groups', ['id'], unique=False)
