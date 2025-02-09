from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.schemas.policy import PolicyCreate, Policy
from app.crud.policy import create_policy, get_all_policies, get_policy_by_id, get_policy_by_version

router = APIRouter()

@router.get("/", response_model=List[Policy])
def get_all_policies(
    db: Session = Depends(get_db)
):
    return get_all_policies(db)

@router.get("/{policy_id}", response_model=Policy)
def get_policy_by_id(
    policy_id: int,
    db: Session = Depends(get_db)
):
    return get_policy_by_id(db, policy_id)

@router.get("/version/{version}", response_model=Policy)
def get_policy_by_version(
    version: str,
    db: Session = Depends(get_db)
):
    return get_policy_by_version(db, version)

@router.post("/", response_model=Policy)
def create_new_policy(
    policy: PolicyCreate,
    db: Session = Depends(get_db)
):
    return create_policy(db, policy)
