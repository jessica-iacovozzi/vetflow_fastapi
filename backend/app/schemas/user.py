from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict
from datetime import datetime
from app.schemas.pet import Pet
from typing import List, Optional

class UserBase(BaseModel):
    email: EmailStr = Field(
        ...,  # Required field
        description="User's email address",
        examples=["user@example.com"]
    )
    full_name: str = Field(
        ..., 
        min_length=2, 
        max_length=100,
        description="Full name of the user",
        json_schema_extra={"examples": ["John Doe"]},
    )
    preferred_language: str = Field(
        default="en", 
        pattern="^(en|fr)$",
        description="Preferred language (en or fr)"
    )
    is_active: bool = True
    pets: List[Pet] = []

    @field_validator('full_name')
    def name_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('Full name cannot be empty')
        return v.strip()

class UserCreate(UserBase):
    password: str = Field(
        ..., 
        min_length=8, 
        max_length=64,
        description="User password",
        json_schema_extra={"examples": ["StrongPassword123!"]},
    )

    @field_validator('password')
    def password_complexity(cls, v):
        import re
        
        # Check minimum requirements
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        
        # At least one uppercase, one lowercase, one number, one special character
        if not re.search(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]+$', v):
            raise ValueError(
                'Password must include: '
                'at least one uppercase letter, '
                'one lowercase letter, '
                'one number, '
                'and one special character'
            )
        
        return v

class UserUpdate(UserBase):
    full_name: Optional[str] = Field(
        default=None, 
        min_length=2, 
        max_length=100
    )
    preferred_language: Optional[str] = Field(
        default=None, 
        pattern="^(en|fr)$"
    )

class User(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

model_config = ConfigDict(from_attributes=True)