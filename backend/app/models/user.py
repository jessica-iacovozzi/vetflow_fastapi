from sqlalchemy import Column, String, Boolean
from sqlalchemy.orm import relationship
from .base import TimeStampedBase

class User(TimeStampedBase):
    __tablename__ = "users"

    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String)
    is_active = Column(Boolean, default=True)
    preferred_language = Column(String, default="en")

    #Relationships
    pets = relationship("Pet", back_populates="owner")