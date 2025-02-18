from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import smtplib
from email.message import EmailMessage
from datetime import datetime

from database import SessionLocal
from models import Dog, User

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def send_email(to_email: str, sender_name: str, sender_email: str, message: str):
    msg = EmailMessage()
    msg['Subject'] = f'Zapytanie dotyczące Twojego psa - {sender_name}'
    msg['From'] = 'kontakt@psidawca.pl'
    msg['To'] = to_email
    msg.set_content(f"Nowa wiadomość od: {sender_name} ({sender_email})\n\n{message}")
    
    with smtplib.SMTP('smtp.yourmailserver.com', 587) as server:
        server.starttls()
        server.login('kontakt@psidawca.pl', 'yourpassword')
        server.send_message(msg)

@router.post("/contact/{dog_id}")
def contact_owner(dog_id: int, sender_name: str, sender_email: str, message: str, db: Session = Depends(get_db)):
    dog = db.query(Dog).filter(Dog.id == dog_id, Dog.is_active == True).first()
    if not dog:
        raise HTTPException(status_code=404, detail="Pies nie znaleziony lub nieaktywny")
    
    owner = db.query(User).filter(User.id == dog.owner_id).first()
    if not owner:
        raise HTTPException(status_code=404, detail="Właściciel nie znaleziony")
    
    if not owner.is_verified:
        raise HTTPException(status_code=400, detail="Właściciel nie zweryfikował konta")
    
    send_email(owner.email, sender_name, sender_email, message)
    
    return {"message": "Wiadomość wysłana do właściciela psa"}
