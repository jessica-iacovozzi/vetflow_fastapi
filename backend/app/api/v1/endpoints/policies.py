from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.user_consent import PolicyCreate, Policy
from app.crud.user_consent import create_policy

router = APIRouter()

@router.post("/", response_model=Policy)
def create_new_policy(
    policy: PolicyCreate,
    db: Session = Depends(get_db)
):
    return create_policy(db, policy)
