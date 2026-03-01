"""Test SQLAlchemy models."""

import pytest
from datetime import datetime
from app.models import ConflictEvent, Source, User, Verification, Alert


def test_create_source(db_session):
    """Test creating a source."""
    source = Source(
        name="Test Source",
        url="https://example.com",
        source_type="api",
        credibility_tier=2,
        credibility_score=0.85
    )
    db_session.add(source)
    db_session.commit()
    db_session.refresh(source)
    
    assert source.id is not None
    assert source.name == "Test Source"
    assert source.is_active is True
    assert source.credibility_tier == 2


def test_create_conflict_event(db_session):
    """Test creating a conflict event."""
    event = ConflictEvent(
        event_type="armed_conflict",
        title="Test Conflict Event",
        description="A test event for validation",
        severity_score=3,
        casualties_min=5,
        casualties_max=10,
        event_timestamp=datetime.utcnow(),
        verification_status="unverified",
        confidence_score=0.65,
        is_active=True,
        country_code="US",
        region_name="Test Region"
    )
    db_session.add(event)
    db_session.commit()
    db_session.refresh(event)
    
    assert event.id is not None
    assert event.severity_score == 3
    assert event.verification_status == "unverified"
    assert event.is_active is True


def test_create_user(db_session):
    """Test creating a user."""
    user = User(
        email="test@example.com",
        username="testuser",
        email_verified=False,
        role="free"
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    
    assert user.id is not None
    assert user.email == "test@example.com"
    assert user.role == "free"
    assert user.is_active is True


def test_severity_constraint(db_session):
    """Test severity score constraint (1-5)."""
    # Valid severity
    event = ConflictEvent(
        event_type="protest",
        title="Valid Event",
        severity_score=5,  # Max valid
        event_timestamp=datetime.utcnow()
    )
    db_session.add(event)
    db_session.commit()
    assert event.severity_score == 5


def test_verification_relationship(db_session):
    """Test verification relationship with event and source."""
    # Create source
    source = Source(
        name="Test Source",
        source_type="api",
        credibility_tier=1
    )
    db_session.add(source)
    
    # Create event
    event = ConflictEvent(
        event_type="armed_conflict",
        title="Test Event",
        severity_score=4,
        event_timestamp=datetime.utcnow()
    )
    db_session.add(event)
    db_session.commit()
    db_session.refresh(source)
    db_session.refresh(event)
    
    # Create verification
    verification = Verification(
        conflict_event_id=event.id,
        source_id=source.id,
        source_url="https://example.com/event",
        source_title="Test Report"
    )
    db_session.add(verification)
    db_session.commit()
    
    # Test relationships
    assert len(event.verifications) == 1
    assert len(source.verifications) == 1
    assert verification.conflict_event.id == event.id
    assert verification.source.id == source.id
