from sqlalchemy import Column, String, Integer, Date, ForeignKey, Enum, Float
from sqlalchemy.orm import relationship
import enum
from .base import TimeStampedBase

class Species(str, enum.Enum):
    DOG = "dog"
    CAT = "cat"
    OTHER = "other"

class Sex(str, enum.Enum):
    MALE = "male"
    FEMALE = "female"
    UNKNOWN = "unknown"

class Pet(TimeStampedBase):
    __tablename__ = "pets"
    __mapper_args__ = {"confirm_deleted_rows": False}

    name = Column(String, nullable=False)
    species = Column(Enum(Species), nullable=False)
    breed = Column(String)
    date_of_birth = Column(Date)
    sex = Column(Enum(Sex), default=Sex.UNKNOWN)
    weight = Column(Float)  # in kg
    microchip_number = Column(String, unique=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Relationships
    owner = relationship("User", back_populates="pets")
    questionnaire_responses = relationship("QuestionnaireResponse", back_populates="pet")