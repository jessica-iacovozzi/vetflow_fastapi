from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .base import TimeStampedBase

class UserConsent(TimeStampedBase):
    __tablename__ = "user_consents"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    policy_id = Column(Integer, ForeignKey("policies.id"))
    consent_date = Column(DateTime(timezone=True), server_default=func.now())
    
    user = relationship("User", back_populates="consents")
    policy = relationship("Policy", back_populates="user_consents")