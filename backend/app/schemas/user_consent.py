from pydantic import BaseModel
from datetime import datetime

class PolicyBase(BaseModel):
    version: str
    text: str
    data_purpose: str
    is_active: bool = True

class PolicyCreate(PolicyBase):
    pass

class Policy(PolicyBase):
    id: int
    effective_date: datetime
    
    class Config:
        from_attributes = True

class UserConsentBase(BaseModel):
    user_id: int
    policy_id: int

class UserConsentCreate(UserConsentBase):
    pass

class UserConsent(UserConsentBase):
    id: int
    consent_date: datetime
    policy: Policy
    
    class Config:
        from_attributes = True