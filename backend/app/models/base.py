from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, DateTime
from datetime import datetime, UTC

Base = declarative_base()

class TimeStampedBase(Base):
    __abstract__ = True
    
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.now(UTC))  
    updated_at = Column(DateTime, default=datetime.now(UTC), onupdate=datetime.now(UTC))