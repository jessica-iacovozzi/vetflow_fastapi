from datetime import timedelta
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.config import get_settings
from app.core.security import create_access_token, verify_password
from app.crud.user import get_user_by_email, create_user
from app.crud.user_consent import create_user_consent
from app.crud.policy import get_latest_active_policy
from app.schemas.auth import Token, UserRegister
from app.schemas.user import User
from app.schemas.user_consent import UserConsentCreate

settings = get_settings()
router = APIRouter()

@router.post("/register", response_model=User)
def register(
    user_in: UserRegister,
    db: Session = Depends(get_db)
) -> Any:
    if not user_in.consent_to_policy:
        raise HTTPException(
            status_code=400,
            detail="You must consent to the current policy to register"
        )
    
    try:
        user = get_user_by_email(db, email=user_in.email)
        if user:
            raise HTTPException(
                status_code=400,
                detail="A user with this email already exists."
            )
        user = create_user(db, user_in)
        
        active_policy = get_latest_active_policy(db)
        if not active_policy:
            raise HTTPException(
                status_code=500,
                detail="No active policy found"
            )
        
        create_user_consent(
            db,
            UserConsentCreate(
                user_id=user.id,
                policy_id=active_policy.id
            )
        )
        db.commit()
        return user
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Failed to complete registration: {str(e)}"
        )

@router.post("/login", response_model=Token)
def login(
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    user = get_user_by_email(db, email=form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }