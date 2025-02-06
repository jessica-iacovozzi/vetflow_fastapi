from pydantic import BaseModel, ConfigDict
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
    
    model_config = ConfigDict(from_attributes=True)