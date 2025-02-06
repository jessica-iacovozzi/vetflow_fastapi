from sqlalchemy import Column, Integer, DateTime, String, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .base import TimeStampedBase

class Policy(TimeStampedBase):
    __tablename__ = "policies"
    
    id = Column(Integer, primary_key=True, index=True)
    version = Column(String, unique=True)
    text = Column(String)
    data_purpose = Column(String)
    effective_date = Column(DateTime(timezone=True), server_default=func.now())
    is_active = Column(Boolean, default=True)
    
    user_consents = relationship("UserConsent", back_populates="policy")