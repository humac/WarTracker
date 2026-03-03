from sqlalchemy import Column, BigInteger, String, Text, Integer, Float, Boolean, DateTime, CheckConstraint, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database import Base


class ConflictEvent(Base):
    __tablename__ = "conflict_events"
    
    id = Column(BigInteger, primary_key=True, index=True)
    latitude = Column(Float, nullable=False, index=True)
    longitude = Column(Float, nullable=False, index=True)
    latitude_display = Column(Float)  # Blurred for safety
    longitude_display = Column(Float)  # Blurred for safety
    event_type = Column(String(50), nullable=False, index=True)
    title = Column(String(500), nullable=False)
    description = Column(Text)
    severity_score = Column(Integer, nullable=False, index=True)
    casualties_min = Column(Integer, default=0)
    casualties_max = Column(Integer)
    event_timestamp = Column(DateTime(timezone=True), nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    verification_status = Column(String(20), default='unverified', index=True)  # unverified|verified|disputed
    confidence_score = Column(Float)
    is_active = Column(Boolean, default=True, index=True)
    actors_involved = Column(JSON, default=list)
    country_code = Column(String(2), index=True)
    region_name = Column(String(200), index=True)
    ai_summary = Column(Text)
    conflict_id = Column(String(100), index=True)  # Group related events
    
    # Relationships
    verifications = relationship("Verification", back_populates="conflict_event", cascade="all, delete-orphan")
    alerts = relationship("Alert", back_populates="conflict_event")
    bookmarks = relationship("Bookmark", back_populates="conflict_event", cascade="all, delete-orphan")
    
    __table_args__ = (
        CheckConstraint('severity_score >= 1 AND severity_score <= 5', name='valid_severity'),
        CheckConstraint('confidence_score >= 0.0 AND confidence_score <= 1.0', name='valid_confidence'),
    )
    
    def __repr__(self):
        return f"<ConflictEvent(id={self.id}, title='{self.title}', severity={self.severity_score})>"
