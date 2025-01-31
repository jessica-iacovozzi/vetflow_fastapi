from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.questionnaire import QuestionnaireResponse
from app.schemas.questionnaire import QuestionnaireCreate, QUESTIONNAIRE_TEMPLATES

def create_questionnaire_response(
    db: Session, 
    questionnaire: QuestionnaireCreate
) -> QuestionnaireResponse:
    db_response = QuestionnaireResponse(
        pet_id=questionnaire.pet_id,
        questionnaire_type=questionnaire.questionnaire_type,
        responses=questionnaire.responses
    )
    db.add(db_response)
    db.commit()
    db.refresh(db_response)
    return db_response

def get_pet_questionnaire_responses(
    db: Session, 
    pet_id: int, 
    questionnaire_type: Optional[str] = None
) -> List[QuestionnaireResponse]:
    query = db.query(QuestionnaireResponse).filter(
        QuestionnaireResponse.pet_id == pet_id
    )
    if questionnaire_type:
        query = query.filter(
            QuestionnaireResponse.questionnaire_type == questionnaire_type
        )
    return query.order_by(QuestionnaireResponse.visit_date.desc()).all()

def get_questionnaire_template(
    questionnaire_type: str, 
    language: str = "en"
) -> List[dict]:
    return QUESTIONNAIRE_TEMPLATES.get(
        questionnaire_type, {}
    ).get(language, [])