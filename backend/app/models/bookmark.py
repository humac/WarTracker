from sqlalchemy import Column, BigInteger, Integer, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database import Base


class Bookmark(Base):
    __tablename__ = "bookmarks"
    
    id = Column(BigInteger, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    conflict_event_id = Column(BigInteger, ForeignKey("conflict_events.id", ondelete="CASCADE"), nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="bookmarks")
    conflict_event = relationship("ConflictEvent", back_populates="bookmarks")
    
    __table_args__ = (
        UniqueConstraint('user_id', 'conflict_event_id', name='uix_user_event'),
    )
    
    def __repr__(self):
        return f"<Bookmark(user_id={self.user_id}, event_id={self.conflict_event_id})>"
