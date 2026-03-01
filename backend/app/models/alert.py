from sqlalchemy import Column, BigInteger, String, Integer, Boolean, DateTime, ForeignKey, CheckConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database import Base


class Alert(Base):
    __tablename__ = "alerts"
    
    id = Column(BigInteger, primary_key=True, index=True)
    user_id = Column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    conflict_event_id = Column(BigInteger, ForeignKey("conflict_events.id"), index=True)
    name = Column(String(200))
    region_filter = Column(JSONB)  # {country_codes: [...], region_names: [...]}
    conflict_type_filter = Column(JSONB)  # Array of event types
    severity_threshold = Column(Integer, default=3)  # 1-5
    notification_method = Column(String(20), default='push')  # push|email|rss
    is_active = Column(Boolean, default=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_triggered = Column(DateTime(timezone=True))
    trigger_count = Column(Integer, default=0)
    
    # Relationships
    user = relationship("User", back_populates="alerts")
    conflict_event = relationship("ConflictEvent", back_populates="alerts")
    
    __table_args__ = (
        CheckConstraint('severity_threshold >= 1 AND severity_threshold <= 5', name='valid_severity_threshold'),
    )
    
    def __repr__(self):
        return f"<Alert(id={self.id}, user_id={self.user_id}, threshold={self.severity_threshold})>"
