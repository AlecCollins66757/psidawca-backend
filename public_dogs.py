from fastapi import APIRouter, Form, Depends
from sqlalchemy.orm import Session
from models import Dog, get_db

router = APIRouter()

@router.post("/dogs/add")
def add_dog(
    name: str = Form(...),
    chip_number: str = Form(...),
    breed: str = Form(...),
    blood_type: str = Form(...),
    weight: float = Form(...),
    birth_date: str = Form(...),
    last_vaccination: str = Form(...),
    city: str = Form(...),
    region: str = Form(...),
    db: Session = Depends(get_db)
):
    """
    Endpoint do dodawania psa do bazy.
    """
    new_dog = Dog(
        name=name,
        chip_number=chip_number,
        breed=breed,
        blood_type=blood_type,
        weight=weight,
        birth_date=birth_date,
        last_vaccination=last_vaccination,
        city=city,
        region=region
    )
    
    db.add(new_dog)
    db.commit()
    db.refresh(new_dog)
    
    return {"message": "Pies został dodany do bazy!", "dog_id": new_dog.id}
