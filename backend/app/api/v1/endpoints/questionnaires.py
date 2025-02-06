from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import get_current_user
from app.db.session import get_db
from app.crud import questionnaire as questionnaire_crud
from app.crud import pet as pet_crud
from app.schemas.questionnaire import (
    Questionnaire, 
    QuestionnaireCreate, 
    QuestionnaireType
)
from app.models.user import User

router = APIRouter()

@router.post("/", response_model=Questionnaire)
def create_questionnaire_response(
    questionnaire_in: QuestionnaireCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Verify pet belongs to current user
    pet = pet_crud.get_pet(db, questionnaire_in.pet_id)
    if not pet or pet.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Pet not found")
    
    return questionnaire_crud.create_questionnaire_response(db, questionnaire_in)

@router.get("/templates/{questionnaire_type}")
def get_questionnaire_template(
    questionnaire_type: QuestionnaireType,
    language: str = "en"
):
    return questionnaire_crud.get_questionnaire_template(
        questionnaire_type, 
        language
    )

@router.get("/pet/{pet_id}", response_model=List[Questionnaire])
def get_pet_questionnaire_responses(
    pet_id: int,
    questionnaire_type: Optional[QuestionnaireType] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Verify pet belongs to current user
    pet = pet_crud.get_pet(db, pet_id)
    if not pet or pet.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Pet not found")
    
    return questionnaire_crud.get_pet_questionnaire_responses(
        db, 
        pet_id, 
        questionnaire_type
    )