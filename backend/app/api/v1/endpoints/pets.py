from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api.deps import get_current_user
from app.db.session import get_db
from app.crud import pet as pet_crud
from app.schemas.pet import Pet, PetCreate, PetUpdate
from app.models.user import User

router = APIRouter()

@router.get("/all", response_model=List[Pet])
def read_all_pets(
    db: Session = Depends(get_db)
) -> List[Pet]:
    """Get all pets in the system."""
    return pet_crud.get_all_pets(db)

@router.get("/", response_model=List[Pet])
def read_pets_by_user(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> List[Pet]:
    """Get all pets owned by the current user."""
    return pet_crud.get_pets_by_owner(db, current_user.id)

@router.get("/owner/{owner_id}", response_model=List[Pet])
def read_pets_by_owner(
    owner_id: int,
    db: Session = Depends(get_db)
) -> List[Pet]:
    """Get all pets owned by a specific user."""
    return pet_crud.get_pets_by_owner(db, owner_id)

@router.get("/{pet_id}", response_model=Pet)
def read_pet(
    pet_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Pet:
    """Get a specific pet by ID."""
    pet = pet_crud.get_pet(db, pet_id)
    if not pet or pet.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Pet not found")
    return pet

@router.post("/", response_model=Pet)
def create_pet(
    pet_data: PetCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Pet:
    """Create a new pet for the current user."""
    pet = pet_crud.create_pet(
        db=db,
        pet_data=pet_data.model_dump(),
        owner_id=current_user.id
    )
    return pet

@router.put("/{pet_id}", response_model=Pet)
def update_pet(
    pet_id: int,
    pet_in: PetUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Pet:
    """Update a pet's information."""
    pet = pet_crud.get_pet(db, pet_id)
    if not pet or pet.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Pet not found")
    
    return pet_crud.update_pet(db, pet_id, pet_in)

@router.delete("/{pet_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_pet(
    pet_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a pet."""
    pet = pet_crud.get_pet(db, pet_id)
    if not pet or pet.owner_id != current_user.id:
        raise HTTPException(status_code=404, detail="Pet not found")
    
    pet_crud.delete_pet(db, pet_id)