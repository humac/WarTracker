from sqlalchemy import Column, BigInteger, String, Integer, Float, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database import Base


class Source(Base):
    __tablename__ = "sources"
    
    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String(200), unique=True, nullable=False)
    url = Column(String(500))
    source_type = Column(String(20), nullable=False)  # api|rss|manual|social
    credibility_tier = Column(Integer, default=3)  # 1-4
    credibility_score = Column(Float, default=0.5)  # 0.0-1.0
    is_active = Column(Boolean, default=True, index=True)
    last_checked = Column(DateTime(timezone=True))
    total_reports = Column(Integer, default=0)
    verified_reports = Column(Integer, default=0)
    api_endpoint = Column(String(500))
    api_key_encrypted = Column(String(500))  # Encrypted API key
    polling_interval_seconds = Column(Integer, default=300)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    verifications = relationship("Verification", back_populates="source")
    
    __table_args__ = (
        # Check constraints handled in migration
    )
    
    def __repr__(self):
        return f"<Source(id={self.id}, name='{self.name}', tier={self.credibility_tier})>"
