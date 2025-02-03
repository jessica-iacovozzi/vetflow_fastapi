from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.user_consent import PolicyCreate, Policy
from app.crud.user_consent import create_policy, check_user_consent_status

router = APIRouter()
@router.post("/policies/", response_model=Policy)
def create_new_policy(
    policy: PolicyCreate,
    db: Session = Depends(get_db)
):
    return create_policy(db, policy)

@router.get("/users/{user_id}/consent-status")
def check_user_consent(
    user_id: int,
    db: Session = Depends(get_db)
):
    return check_user_consent_status(db, user_id)