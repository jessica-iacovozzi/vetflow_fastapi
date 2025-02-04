from sqlalchemy.orm import Session
from typing import List, Optional
from fastapi import HTTPException
from app.models.user_consent import UserConsent, Policy
from app.schemas.user_consent import PolicyCreate

def get_active_policy(db: Session) -> Optional[Policy]:
    return db.query(Policy).filter(Policy.is_active == True).first()

def create_policy(db: Session, policy: PolicyCreate) -> Policy:
    # If this is a new active policy, deactivate all other policies
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

def create_user_consent(
    db: Session, 
    user_id: int, 
    policy_id: int
) -> UserConsent:
    db_consent = UserConsent(
        user_id=user_id,
        policy_id=policy_id
    )
    db.add(db_consent)
    try:
        db.commit()
        db.refresh(db_consent)
        return db_consent
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

def get_user_consents(
    db: Session, 
    user_id: int
) -> List[UserConsent]:
    return db.query(UserConsent).filter(
        UserConsent.user_id == user_id
    ).all()

def get_latest_user_consent(
    db: Session, 
    user_id: int
) -> Optional[UserConsent]:
    return db.query(UserConsent).filter(
        UserConsent.user_id == user_id
    ).order_by(UserConsent.consent_date.desc()).first()

def check_user_consent_status(
    db: Session, 
    user_id: int
) -> dict:
    """
    Check if user has consented to the latest active policy.
    Returns a dict with consent status and details.
    """
    active_policy = get_active_policy(db)
    if not active_policy:
        return {
            "needs_consent": False,
            "reason": "No active policy found"
        }
    
    latest_consent = get_latest_user_consent(db, user_id)
    if not latest_consent:
        return {
            "needs_consent": True,
            "reason": "No previous consent found"
        }
    
    if latest_consent.policy_id != active_policy.id:
        return {
            "needs_consent": True,
            "reason": "New policy requires consent",
            "current_policy_version": latest_consent.policy.version,
            "new_policy_version": active_policy.version
        }
    
    return {
        "needs_consent": False,
        "reason": "User has consented to current policy"
    }

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