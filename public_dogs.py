from fastapi import APIRouter, Form, Depends, Request
from sqlalchemy.orm import Session
from models import Dog,
from fastapi.templating import Jinja2Templates
from database import get_db  # Importujemy get_db z database.py

router = APIRouter()

templates = Jinja2Templates(directory="templates")

@router.post("/dogs/add")
async def add_dog(
    request: Request,
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
    
    return templates.TemplateResponse(
        "register_dog.html", 
        {"request": request, "message": "Pies został dodany do bazy!"}
    )
