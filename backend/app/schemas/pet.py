from pydantic import BaseModel, Field
from datetime import date, datetime
from typing import Optional
from enum import Enum

class Species(str, Enum):
    DOG = "dog"
    CAT = "cat"
    OTHER = "other"

class Sex(str, Enum):
    MALE = "male"
    FEMALE = "female"
    UNKNOWN = "unknown"

class PetBase(BaseModel):
    name: str
    species: Species
    breed: Optional[str] = None
    date_of_birth: Optional[date] = None
    sex: Sex = Sex.UNKNOWN
    weight: Optional[float] = None
    microchip_number: Optional[str] = None

class PetCreate(PetBase):
    pass

class PetUpdate(PetBase):
    name: Optional[str] = None
    species: Optional[Species] = None

class Pet(PetBase):
    id: int
    owner_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True