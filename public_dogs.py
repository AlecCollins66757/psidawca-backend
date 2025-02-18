from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Optional

from database import SessionLocal
from models import Dog

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/dogs", response_model=List[dict])
def get_public_dogs(
    region: Optional[str] = None, city: Optional[str] = None, blood_type: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Dog).filter(Dog.is_active == True)
    
    if region:
        query = query.filter(Dog.region == region)
    if city:
        query = query.filter(Dog.city == city)
    if blood_type:
        query = query.filter(Dog.blood_type == blood_type)
    
    dogs = query.all()
    return [
        {
            "id": dog.id,
            "name": dog.name,
            "region": dog.region,
            "city": dog.city,
            "blood_type": dog.blood_type
        } for dog in dogs
    ]
