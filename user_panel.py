from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import date

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

@router.post("/dogs/add")
def add_dog(
    name: str, chip_number: str, breed: str, blood_type: str, birth_date: date,
    weight: float, city: str, region: str, last_vaccination: date,
    user: User = Depends(read_users_me), db: Session = Depends(get_db)
):
    existing_dog = db.query(Dog).filter(Dog.chip_number == chip_number).first()
    if existing_dog:
        raise HTTPException(status_code=400, detail="Pies z tym numerem chip już istnieje")
    
    dog = Dog(
        name=name, chip_number=chip_number, breed=breed, blood_type=blood_type,
        birth_date=birth_date, weight=weight, city=city, region=region,
        last_vaccination=last_vaccination, owner_id=user.id
    )
    db.add(dog)
    db.commit()
    db.refresh(dog)
    return {"message": "Pies dodany do bazy", "dog_id": dog.id}

@router.get("/dogs/my", response_model=List[Dog])
def get_my_dogs(user: User = Depends(read_users_me), db: Session = Depends(get_db)):
    return db.query(Dog).filter(Dog.owner_id == user.id).all()

@router.put("/dogs/update/{dog_id}")
def update_dog(
    dog_id: int, name: str, breed: str, blood_type: str, birth_date: date,
    weight: float, city: str, region: str, last_vaccination: date,
    user: User = Depends(read_users_me), db: Session = Depends(get_db)
):
    dog = db.query(Dog).filter(Dog.id == dog_id, Dog.owner_id == user.id).first()
    if not dog:
        raise HTTPException(status_code=404, detail="Pies nie znaleziony lub brak dostępu")
    
    dog.name = name
    dog.breed = breed
    dog.blood_type = blood_type
    dog.birth_date = birth_date
    dog.weight = weight
    dog.city = city
    dog.region = region
    dog.last_vaccination = last_vaccination
    
    db.commit()
    return {"message": "Dane psa zaktualizowane"}

@router.delete("/dogs/delete/{dog_id}")
def delete_dog(dog_id: int, user: User = Depends(read_users_me), db: Session = Depends(get_db)):
    dog = db.query(Dog).filter(Dog.id == dog_id, Dog.owner_id == user.id).first()
    if not dog:
        raise HTTPException(status_code=404, detail="Pies nie znaleziony lub brak dostępu")
    
    db.delete(dog)
    db.commit()
    return {"message": "Pies usunięty z bazy"}
