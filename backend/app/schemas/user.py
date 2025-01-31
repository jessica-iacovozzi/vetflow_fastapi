from pydantic import BaseModel, EmailStr
from datetime import datetime
from app.schemas.pet import Pet
from typing import List

class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    preferred_language: str = "en"
    is_active: bool = True
    pets: List[Pet] = []

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # This enables ORM mode