from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import SessionLocal
from models import Dog, User
from login import read_users_me

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def is_admin(user: User):
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Brak uprawnień administratora")

@router.get("/admin/users", response_model=List[dict])
def get_all_users(user: User = Depends(read_users_me), db: Session = Depends(get_db)):
    is_admin(user)
    users = db.query(User).all()
    return [{"id": u.id, "email": u.email, "is_active": u.is_active, "is_verified": u.is_verified} for u in users]

@router.delete("/admin/users/{user_id}")
def delete_user(user_id: int, user: User = Depends(read_users_me), db: Session = Depends(get_db)):
    is_admin(user)
    user_to_delete = db.query(User).filter(User.id == user_id).first()
    if not user_to_delete:
        raise HTTPException(status_code=404, detail="Użytkownik nie znaleziony")
    
    db.delete(user_to_delete)
    db.commit()
    return {"message": "Użytkownik usunięty"}

@router.get("/admin/dogs", response_model=List[dict])
def get_all_dogs(user: User = Depends(read_users_me), db: Session = Depends(get_db)):
    is_admin(user)
    dogs = db.query(Dog).all()
    return [{"id": d.id, "name": d.name, "is_active": d.is_active, "owner_id": d.owner_id} for d in dogs]

@router.put("/admin/dogs/approve/{dog_id}")
def approve_dog(dog_id: int, user: User = Depends(read_users_me), db: Session = Depends(get_db)):
    is_admin(user)
    dog = db.query(Dog).filter(Dog.id == dog_id).first()
    if not dog:
        raise HTTPException(status_code=404, detail="Pies nie znaleziony")
    
    dog.is_active = True
    db.commit()
    return {"message": "Pies zatwierdzony"}

@router.delete("/admin/dogs/{dog_id}")
def delete_dog(dog_id: int, user: User = Depends(read_users_me), db: Session = Depends(get_db)):
    is_admin(user)
    dog = db.query(Dog).filter(Dog.id == dog_id).first()
    if not dog:
        raise HTTPException(status_code=404, detail="Pies nie znaleziony")
    
    db.delete(dog)
    db.commit()
    return {"message": "Pies usunięty z bazy"}
