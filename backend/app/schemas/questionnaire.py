from pydantic import BaseModel, Field
from typing import Dict, Any, Optional
from datetime import datetime
from enum import Enum

class QuestionnaireType(str, Enum):
    GENERAL_CHECKUP = "general_checkup"
    VACCINATION = "vaccination"
    SPECIFIC_CONCERN = "specific_concern"
    EMERGENCY = "emergency"

class QuestionnaireBase(BaseModel):
    questionnaire_type: QuestionnaireType
    responses: Dict[str, Any]

class QuestionnaireCreate(QuestionnaireBase):
    pet_id: int

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