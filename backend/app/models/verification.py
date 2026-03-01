from sqlalchemy import Column, BigInteger, String, Text, DateTime, ForeignKey, UniqueConstraint, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database import Base


class Verification(Base):
    __tablename__ = "verifications"
    
    id = Column(BigInteger, primary_key=True, index=True)
    conflict_event_id = Column(BigInteger, ForeignKey("conflict_events.id", ondelete="CASCADE"), nullable=False, index=True)
    source_id = Column(BigInteger, ForeignKey("sources.id"), nullable=False, index=True)
    source_url = Column(String(1000))
    source_title = Column(String(500))
    source_excerpt = Column(Text)
    verified_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    verification_method = Column(String(20), default='auto')  # auto|manual
    source_casualties_min = Column(Integer)
    source_casualties_max = Column(Integer)
    
    # Relationships
    conflict_event = relationship("ConflictEvent", back_populates="verifications")
    source = relationship("Source", back_populates="verifications")
    
    __table_args__ = (
        UniqueConstraint('conflict_event_id', 'source_id', name='uix_event_source'),
    )
    
    def __repr__(self):
        return f"<Verification(event_id={self.conflict_event_id}, source_id={self.source_id})>"
