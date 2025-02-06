from sqlalchemy import desc
from sqlalchemy.orm import Session
from app.models.policy import Policy
from datetime import datetime, timezone
from app.schemas.policy import PolicyCreate
from fastapi import HTTPException
from typing import Optional, List

def get_latest_active_policy(db: Session) -> Policy:
    return db.query(Policy)\
        .filter(Policy.is_active == True)\
        .filter(Policy.effective_date <= datetime.now(timezone.utc))\
        .order_by(desc(Policy.effective_date))\
        .first()


def get_all_policies(
    db: Session, 
    skip: int = 0, 
    limit: int = 100
) -> List[Policy]:
    return db.query(Policy).offset(skip).limit(limit).all()

def get_policy_by_version(
    db: Session, 
    version: str
) -> Optional[Policy]:
    return db.query(Policy).filter(Policy.version == version).first()

def create_policy(db: Session, policy: PolicyCreate) -> Policy:
    if policy.is_active:
        db.query(Policy).filter(Policy.is_active == True).update(
            {"is_active": False}
        )
    
    db_policy = Policy(**policy.model_dump())
    db.add(db_policy)
    try:
        db.commit()
        db.refresh(db_policy)
        return db_policy
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))