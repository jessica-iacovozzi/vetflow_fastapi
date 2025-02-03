from sqlalchemy import Column, Integer, ForeignKey, DateTime, String, Boolean
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

class UserConsent(TimeStampedBase):
    __tablename__ = "user_consents"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    policy_id = Column(Integer, ForeignKey("policies.id"))
    consent_date = Column(DateTime(timezone=True), server_default=func.now())
    
    user = relationship("User", back_populates="consents")
    policy = relationship("Policy", back_populates="user_consents")