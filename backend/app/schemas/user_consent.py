from pydantic import BaseModel, ConfigDict
from datetime import datetime
from app.schemas.policy import Policy

class UserConsentBase(BaseModel):
    user_id: int
    policy_id: int

class UserConsentCreate(UserConsentBase):
    pass

class UserConsent(UserConsentBase):
    id: int
    consent_date: datetime
    policy: Policy
    
    model_config = ConfigDict(from_attributes=True)