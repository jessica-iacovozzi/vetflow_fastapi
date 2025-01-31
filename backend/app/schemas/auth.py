from pydantic import BaseModel, EmailStr
from typing import Optional

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class UserAuth(BaseModel):
    email: EmailStr
    password: str

class UserRegister(UserAuth):
    full_name: str
    preferred_language: str = "en"