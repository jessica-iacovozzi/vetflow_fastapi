from pydantic import BaseModel, Field, field_validator
from datetime import date, datetime
from typing import Optional
from enum import Enum

class Species(str, Enum):
    DOG = "dog"
    CAT = "cat"
    BIRD = "bird"
    RABBIT = "rabbit"
    OTHER = "other"

class Sex(str, Enum):
    MALE = "male"
    FEMALE = "female"
    UNKNOWN = "unknown"

class PetBase(BaseModel):
    name: str = Field(
        ..., 
        min_length=1, 
        max_length=50,
        description="Pet's name",
        examples=["Fluffy", "Max"]
    )
    species: Species = Field(
        ..., 
        description="Species of the pet"
    )
    breed: Optional[str] = Field(
        default=None, 
        max_length=100,
        description="Breed of the pet",
        examples=["Golden Retriever", "Siamese"]
    )
    date_of_birth: Optional[date] = Field(
        default=None,
        description="Pet's date of birth"
    )
    sex: Sex = Field(
        default=Sex.UNKNOWN, 
        description="Sex of the pet"
    )
    weight: Optional[float] = Field(
        default=None, 
        ge=0, 
        le=500,  # Assuming max weight of 500 kg for extreme cases
        description="Weight of the pet in kilograms"
    )
    microchip_number: Optional[str] = Field(
        default=None, 
        max_length=50,
        description="Microchip identification number"
    )

    @field_validator('date_of_birth')
    def validate_birth_date(cls, v):
        if v and v > date.today():
            raise ValueError('Birth date cannot be in the future')
        return v

    @field_validator('name')
    def validate_name(cls, v):
        # Ensure name contains only letters and spaces
        if not all(char.isalpha() or char.isspace() for char in v):
            raise ValueError('Pet name must contain only letters and spaces')
        return v.strip()

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