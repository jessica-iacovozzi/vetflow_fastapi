from pydantic import BaseModel, Field, field_validator
from typing import Dict, Any, Optional
from datetime import datetime
from enum import Enum

class QuestionnaireType(str, Enum):
    GENERAL_CHECKUP = "general_checkup"
    VACCINATION = "vaccination"
    SPECIFIC_CONCERN = "specific_concern"
    EMERGENCY = "emergency"

class QuestionnaireBase(BaseModel):
    questionnaire_type: QuestionnaireType = Field(
        ..., 
        description="Type of veterinary questionnaire"
    )
    responses: Dict[str, Any] = Field(
        ..., 
        description="Responses to questionnaire",
        min_items=1
    )

    @field_validator('responses')
    def validate_responses(cls, responses, values):
        # Get the template for the specific questionnaire type
        from app.crud.questionnaire import get_questionnaire_template
        questionnaire_type = values.data.get('questionnaire_type')
        
        # Get template for the questionnaire type
        template = get_questionnaire_template(questionnaire_type)
        
        # Validate responses against template
        for question in template:
            response = responses.get(question['id'])
            
            # Validate multiple choice
            if question['type'] == 'multiple_choice':
                if response and response not in question.get('options', []):
                    raise ValueError(f"Invalid response for {question['id']}")
            
            # Validate multiple select
            elif question['type'] == 'multiple_select':
                if response:
                    if not isinstance(response, list):
                        raise ValueError(f"Response for {question['id']} must be a list")
                    if not all(opt in question.get('options', []) for opt in response):
                        raise ValueError(f"Invalid options for {question['id']}")
        
        return responses

class QuestionnaireCreate(QuestionnaireBase):
    pet_id: int = Field(
        ..., 
        gt=0, 
        description="ID of the pet associated with this questionnaire"
    )

class Questionnaire(QuestionnaireBase):
    id: int
    pet_id: int
    visit_date: datetime

    class Config:
        from_attributes = True

# Predefined Questionnaire Templates
QUESTIONNAIRE_TEMPLATES = {
    QuestionnaireType.GENERAL_CHECKUP: {
        "en": [
            {
                "id": "appetite",
                "type": "multiple_choice",
                "question": "How is your pet's appetite?",
                "options": [
                    "Normal", 
                    "Decreased", 
                    "Increased", 
                    "Not eating"
                ]
            },
            {
                "id": "energy_level",
                "type": "multiple_choice",
                "question": "How would you describe your pet's energy level?",
                "options": [
                    "Very active", 
                    "Normal", 
                    "Lethargic", 
                    "Very quiet"
                ]
            }
        ],
        "fr": [
            {
                "id": "appetite",
                "type": "multiple_choice",
                "question": "Quel est l'appétit de votre animal ?",
                "options": [
                    "Normal", 
                    "Diminué", 
                    "Augmenté", 
                    "Ne mange pas"
                ]
            },
            {
                "id": "energy_level",
                "type": "multiple_choice",
                "question": "Comment décririez-vous le niveau d'activité de votre animal ?",
                "options": [
                    "Très actif", 
                    "Normal", 
                    "Lethargique", 
                    "Inactif"
                ]
            }
        ]
    },
    QuestionnaireType.EMERGENCY: {
        "en": [
            {
                "id": "emergency_symptoms",
                "type": "multiple_select",
                "question": "Select all symptoms your pet is experiencing:",
                "options": [
                    "Vomiting",
                    "Diarrhea", 
                    "Not eating",
                    "Lethargy",
                    "Difficulty breathing",
                    "Bleeding",
                    "Seizures"
                ]
            }
        ],
        "fr": [
            {
                "id": "emergency_symptoms",
                "type": "multiple_select",
                "question": "Sélectionnez tous les symptômes que votre animal présente :",
                "options": [
                    "Vomissements",
                    "Diarrhée", 
                    "Ne mange pas",
                    "Léthargique",
                    "Difficulté à respirer",
                    "Saignement",
                    "Convulsions"
                ]
            }
        ]
    }
}