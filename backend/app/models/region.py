from sqlalchemy import Column, BigInteger, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database import Base


class Region(Base):
    __tablename__ = "regions"
    
    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    country_code = Column(String(2), index=True)
    boundary_wkt = Column(Text)  # WKT format for polygon boundaries (optional)
    region_type = Column(String(50), default='country')  # country|province|custom
    parent_region_id = Column(BigInteger, ForeignKey("regions.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Self-referential relationship for hierarchical regions
    parent = relationship("Region", remote_side=[id], backref="children")
    
    def __repr__(self):
        return f"<Region(id={self.id}, name='{self.name}', type='{self.region_type}')>"
