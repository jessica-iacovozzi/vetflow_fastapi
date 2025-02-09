from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.pet import Pet
from app.schemas.pet import PetCreate, PetUpdate

def create_pet(db: Session, pet_data: PetCreate, owner_id: int) -> Pet:
    db_pet = Pet(**pet_data)
    db_pet.owner_id = owner_id
    db.add(db_pet)
    db.commit()
    db.refresh(db_pet)
    return db_pet

def get_pet(db: Session, pet_id: int) -> Optional[Pet]:
    return db.query(Pet).filter(Pet.id == pet_id).first()

def get_pets_by_owner(db: Session, owner_id: int) -> List[Pet]:
    return db.query(Pet).filter(Pet.owner_id == owner_id).all()

def update_pet(db: Session, pet_id: int, pet: PetUpdate) -> Optional[Pet]:
    db_pet = get_pet(db, pet_id)
    if not db_pet:
        return None
        
    for field, value in pet.model_dump(exclude_unset=True).items():
        setattr(db_pet, field, value)
    
    db.commit()
    db.refresh(db_pet)
    return db_pet

def delete_pet(db: Session, pet_id: int) -> bool:
    db_pet = get_pet(db, pet_id)
    if not db_pet:
        return False
    
    db.delete(db_pet)
    db.commit()
    return True