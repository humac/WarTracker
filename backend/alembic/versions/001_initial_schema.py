"""Initial schema - create all tables

Revision ID: 001
Revises: 
Create Date: 2026-03-01

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from geoalchemy2 import Geometry


# revision identifiers, used by Alembic.
revision: str = '001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create sources table
    op.create_table('sources',
        sa.Column('id', sa.BigInteger(), sa.Identity(), nullable=False),
        sa.Column('name', sa.String(200), nullable=False),
        sa.Column('url', sa.String(500), nullable=True),
        sa.Column('source_type', sa.String(20), nullable=False),
        sa.Column('credibility_tier', sa.Integer(), nullable=True),
        sa.Column('credibility_score', sa.Float(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True, default=True),
        sa.Column('last_checked', sa.DateTime(timezone=True), nullable=True),
        sa.Column('total_reports', sa.Integer(), nullable=True, default=0),
        sa.Column('verified_reports', sa.Integer(), nullable=True, default=0),
        sa.Column('api_endpoint', sa.String(500), nullable=True),
        sa.Column('api_key_encrypted', sa.String(500), nullable=True),
        sa.Column('polling_interval_seconds', sa.Integer(), nullable=True, default=300),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name'),
        sa.CheckConstraint('credibility_tier >= 1 AND credibility_tier <= 4', name='valid_tier'),
        sa.CheckConstraint('credibility_score >= 0.0 AND credibility_score <= 1.0', name='valid_credibility_score'),
    )
    op.create_index('idx_sources_active', 'sources', ['is_active'], unique=False)
    op.create_index('idx_sources_tier', 'sources', ['credibility_tier'], unique=False)

    # Create regions table
    op.create_table('regions',
        sa.Column('id', sa.BigInteger(), sa.Identity(), nullable=False),
        sa.Column('name', sa.String(200), nullable=False),
        sa.Column('country_code', sa.String(2), nullable=True),
        sa.Column('boundary', Geometry('POLYGON', srid=4326), nullable=True),
        sa.Column('region_type', sa.String(50), nullable=True, default='country'),
        sa.Column('parent_region_id', sa.BigInteger(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.ForeignKeyConstraint(['parent_region_id'], ['regions.id'], ),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('idx_regions_boundary', 'regions', ['boundary'], unique=False, postgresql_using='gist')
    op.create_index('idx_regions_country', 'regions', ['country_code'], unique=False)
    op.create_index('idx_regions_type', 'regions', ['region_type'], unique=False)

    # Create conflict_events table
    op.create_table('conflict_events',
        sa.Column('id', sa.BigInteger(), sa.Identity(), nullable=False),
        sa.Column('location', Geometry('POINT', srid=4326), nullable=False),
        sa.Column('location_display', Geometry('POINT', srid=4326), nullable=True),
        sa.Column('event_type', sa.String(50), nullable=False),
        sa.Column('title', sa.String(500), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('severity_score', sa.Integer(), nullable=False),
        sa.Column('casualties_min', sa.Integer(), nullable=True, default=0),
        sa.Column('casualties_max', sa.Integer(), nullable=True),
        sa.Column('event_timestamp', sa.DateTime(timezone=True), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.Column('verification_status', sa.String(20), nullable=True, default='unverified'),
        sa.Column('confidence_score', sa.Float(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True, default=True),
        sa.Column('actors_involved', sa.JSON(), nullable=True, default=list),
        sa.Column('country_code', sa.String(2), nullable=True),
        sa.Column('region_name', sa.String(200), nullable=True),
        sa.Column('ai_summary', sa.Text(), nullable=True),
        sa.Column('conflict_id', sa.String(100), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.CheckConstraint('severity_score >= 1 AND severity_score <= 5', name='valid_severity'),
        sa.CheckConstraint('confidence_score >= 0.0 AND confidence_score <= 1.0', name='valid_confidence'),
    )
    op.create_index('idx_conflict_events_location', 'conflict_events', ['location'], unique=False, postgresql_using='gist')
    op.create_index('idx_conflict_events_active_severity', 'conflict_events', ['is_active', 'severity_score'], unique=False)
    op.create_index('idx_conflict_events_timestamp', 'conflict_events', ['event_timestamp'], unique=False)
    op.create_index('idx_conflict_events_country', 'conflict_events', ['country_code'], unique=False)
    op.create_index('idx_conflict_events_region', 'conflict_events', ['region_name'], unique=False)
    op.create_index('idx_conflict_events_type', 'conflict_events', ['event_type'], unique=False)
    op.create_index('idx_conflict_events_verification', 'conflict_events', ['verification_status'], unique=False)

    # Create users table
    op.create_table('users',
        sa.Column('id', sa.BigInteger(), sa.Identity(), nullable=False),
        sa.Column('email', sa.String(255), nullable=False),
        sa.Column('password_hash', sa.String(255), nullable=True),
        sa.Column('username', sa.String(100), nullable=True),
        sa.Column('email_verified', sa.Boolean(), nullable=True, default=False),
        sa.Column('role', sa.String(20), nullable=True, default='free'),
        sa.Column('oauth_provider', sa.String(50), nullable=True),
        sa.Column('oauth_id', sa.String(255), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.Column('last_login', sa.DateTime(timezone=True), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True, default=True),
        sa.Column('failed_login_attempts', sa.Integer(), nullable=True, default=0),
        sa.Column('locked_until', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email'),
        sa.UniqueConstraint('username'),
    )
    op.create_index('idx_users_email', 'users', ['email'], unique=False)
    op.create_index('idx_users_role', 'users', ['role'], unique=False)
    op.create_index('idx_users_active', 'users', ['is_active'], unique=False)

    # Create verifications table
    op.create_table('verifications',
        sa.Column('id', sa.BigInteger(), sa.Identity(), nullable=False),
        sa.Column('conflict_event_id', sa.BigInteger(), nullable=False),
        sa.Column('source_id', sa.BigInteger(), nullable=False),
        sa.Column('source_url', sa.String(1000), nullable=True),
        sa.Column('source_title', sa.String(500), nullable=True),
        sa.Column('source_excerpt', sa.Text(), nullable=True),
        sa.Column('verified_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.Column('verification_method', sa.String(20), nullable=True, default='auto'),
        sa.Column('source_casualties_min', sa.Integer(), nullable=True),
        sa.Column('source_casualties_max', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['conflict_event_id'], ['conflict_events.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['source_id'], ['sources.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('conflict_event_id', 'source_id', name='uix_event_source'),
    )
    op.create_index('idx_verifications_event', 'verifications', ['conflict_event_id'], unique=False)
    op.create_index('idx_verifications_source', 'verifications', ['source_id'], unique=False)
    op.create_index('idx_verifications_method', 'verifications', ['verification_method'], unique=False)

    # Create alerts table
    op.create_table('alerts',
        sa.Column('id', sa.BigInteger(), sa.Identity(), nullable=False),
        sa.Column('user_id', sa.BigInteger(), nullable=False),
        sa.Column('conflict_event_id', sa.BigInteger(), nullable=True),
        sa.Column('name', sa.String(200), nullable=True),
        sa.Column('region_filter', sa.JSON(), nullable=True),
        sa.Column('conflict_type_filter', sa.JSON(), nullable=True),
        sa.Column('severity_threshold', sa.Integer(), nullable=True, default=3),
        sa.Column('notification_method', sa.String(20), nullable=True, default='push'),
        sa.Column('is_active', sa.Boolean(), nullable=True, default=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.Column('last_triggered', sa.DateTime(timezone=True), nullable=True),
        sa.Column('trigger_count', sa.Integer(), nullable=True, default=0),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['conflict_event_id'], ['conflict_events.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.CheckConstraint('severity_threshold >= 1 AND severity_threshold <= 5', name='valid_severity_threshold'),
    )
    op.create_index('idx_alerts_user', 'alerts', ['user_id'], unique=False)
    op.create_index('idx_alerts_active', 'alerts', ['is_active'], unique=False)
    op.create_index('idx_alerts_severity', 'alerts', ['severity_threshold'], unique=False)

    # Create bookmarks table
    op.create_table('bookmarks',
        sa.Column('id', sa.BigInteger(), sa.Identity(), nullable=False),
        sa.Column('user_id', sa.BigInteger(), nullable=False),
        sa.Column('conflict_event_id', sa.BigInteger(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['conflict_event_id'], ['conflict_events.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id', 'conflict_event_id', name='uix_user_event'),
    )
    op.create_index('idx_bookmarks_user', 'bookmarks', ['user_id'], unique=False)
    op.create_index('idx_bookmarks_event', 'bookmarks', ['conflict_event_id'], unique=False)

    # Create user_preferences table
    op.create_table('user_preferences',
        sa.Column('id', sa.BigInteger(), sa.Identity(), nullable=False),
        sa.Column('user_id', sa.BigInteger(), nullable=False),
        sa.Column('theme', sa.String(20), nullable=True, default='light'),
        sa.Column('default_map_view', sa.JSON(), nullable=True),
        sa.Column('export_format', sa.String(10), nullable=True, default='json'),
        sa.Column('email_notifications', sa.Boolean(), nullable=True, default=True),
        sa.Column('push_notifications', sa.Boolean(), nullable=True, default=True),
        sa.Column('quiet_hours_start', sa.Time(), nullable=True),
        sa.Column('quiet_hours_end', sa.Time(), nullable=True),
        sa.Column('language', sa.String(10), nullable=True, default='en'),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id'),
    )


def downgrade() -> None:
    op.drop_table('user_preferences')
    op.drop_table('bookmarks')
    op.drop_table('alerts')
    op.drop_table('verifications')
    op.drop_table('users')
    op.drop_table('conflict_events')
    op.drop_table('regions')
    op.drop_table('sources')
