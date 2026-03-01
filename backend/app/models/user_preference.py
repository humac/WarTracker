from sqlalchemy import Column, BigInteger, String, Boolean, Time, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database import Base


class UserPreference(Base):
    __tablename__ = "user_preferences"
    
    id = Column(BigInteger, primary_key=True, index=True)
    user_id = Column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    theme = Column(String(20), default='light')  # light|dark
    default_map_view = Column(JSONB)  # {lat, lng, zoom}
    export_format = Column(String(10), default='json')  # csv|json
    email_notifications = Column(Boolean, default=True)
    push_notifications = Column(Boolean, default=True)
    quiet_hours_start = Column(Time)
    quiet_hours_end = Column(Time)
    language = Column(String(10), default='en')
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationship
    user = relationship("User", back_populates="preferences")
    
    def __repr__(self):
        return f"<UserPreference(user_id={self.user_id}, theme='{self.theme}')>"
