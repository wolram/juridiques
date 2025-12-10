"""initial

Revision ID: 0001_initial
Revises: 
Create Date: 2025-12-11 00:00:00.000000
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0001_initial'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('email', sa.String(length=255), nullable=False, unique=True),
        sa.Column('hashed_password', sa.String(length=255)),
        sa.Column('full_name', sa.String(length=255)),
        sa.Column('oab_number', sa.String(length=50)),
        sa.Column('role', sa.String(length=50), nullable=False, server_default='user'),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='1'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )
    # Demais tabelas simplificadas: spaces, threads, messages, processes, audit_logs
    op.create_table(
        'spaces',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('owner_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text()),
        sa.Column('is_public', sa.Boolean(), nullable=False, server_default='0'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )

    op.create_table(
        'processes',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('space_id', sa.Integer(), sa.ForeignKey('spaces.id'), nullable=False),
        sa.Column('cnj_number', sa.String(length=50), nullable=True, unique=True),
        sa.Column('tribunal', sa.String(length=255)),
        sa.Column('classe', sa.String(length=255)),
        sa.Column('partes', sa.Text()),
        sa.Column('status', sa.String(length=50), nullable=False, server_default='pending'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )

    op.create_table(
        'threads',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('owner_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('space_id', sa.Integer(), sa.ForeignKey('spaces.id')),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('process_id', sa.Integer(), sa.ForeignKey('processes.id')),
        sa.Column('status', sa.String(length=50), nullable=False, server_default='draft'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )

    op.create_table(
        'messages',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('thread_id', sa.Integer(), sa.ForeignKey('threads.id'), nullable=False),
        sa.Column('role', sa.String(length=50)),
        sa.Column('content', sa.Text()),
        sa.Column('metadata', sa.JSON()),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )

    op.create_table(
        'audit_logs',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('action', sa.String(length=255)),
        sa.Column('resource_type', sa.String(length=50)),
        sa.Column('resource_id', sa.Integer()),
        sa.Column('details', sa.JSON()),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )


def downgrade():
    op.drop_table('audit_logs')
    op.drop_table('messages')
    op.drop_table('threads')
    op.drop_table('processes')
    op.drop_table('spaces')
    op.drop_table('users')
