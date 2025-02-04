from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.crud.user_consent import check_user_consent_status

router = APIRouter()

@router.get("/{user_id}/consent-status")
def check_user_consent(
    user_id: int,
    db: Session = Depends(get_db)
):
    return check_user_consent_status(db, user_id)