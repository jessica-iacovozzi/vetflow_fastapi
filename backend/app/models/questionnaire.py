from sqlalchemy import Column, Integer, JSON, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
import enum
from datetime import datetime, UTC
from .base import TimeStampedBase

class QuestionnaireType(str, enum.Enum):
    GENERAL_CHECKUP = "general_checkup"
    VACCINATION = "vaccination"
    SPECIFIC_CONCERN = "specific_concern"
    EMERGENCY = "emergency"

class QuestionnaireResponse(TimeStampedBase):
    __tablename__ = "questionnaire_responses"

    pet_id = Column(Integer, ForeignKey("pets.id"), nullable=False)
    questionnaire_type = Column(Enum(QuestionnaireType), nullable=False)
    responses = Column(JSON, nullable=False)
    visit_date = Column(DateTime, default=datetime.now(UTC))
    
    # Relationships
    pet = relationship("Pet", back_populates="questionnaire_responses")
