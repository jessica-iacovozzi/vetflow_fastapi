from fastapi import APIRouter
from app.api.v1.endpoints import users, auth, pets, questionnaires

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(pets.router, prefix="/pets", tags=["pets"])
api_router.include_router(questionnaires.router, prefix="/questionnaires", tags=["questionnaires"])