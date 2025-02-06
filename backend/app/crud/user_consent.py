from sqlalchemy.orm import Session
from typing import List, Optional
from fastapi import HTTPException
from app.models.user_consent import UserConsent
from app.schemas.user_consent import UserConsentCreate
from app.crud.policy import get_latest_active_policy

def create_user_consent(
    db: Session, 
    user_consent: UserConsentCreate
) -> UserConsent:
    db_consent = UserConsent(
        user_id=user_consent.user_id,
        policy_id=user_consent.policy_id
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
    active_policy = get_latest_active_policy(db)
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