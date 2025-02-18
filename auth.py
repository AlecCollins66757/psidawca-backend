from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext
import smtplib
from email.message import EmailMessage

from database import SessionLocal
from models import User

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def send_verification_email(email: str, token: str):
    msg = EmailMessage()
    msg['Subject'] = 'Potwierdź swoje konto'
    msg['From'] = 'kontakt@psidawca.pl'
    msg['To'] = email
    msg.set_content(f"Kliknij w link, aby potwierdzić swoje konto: https://psidawca.pl/verify/{token}")
    
    with smtplib.SMTP('smtp.yourmailserver.com', 587) as server:
        server.starttls()
        server.login('kontakt@psidawca.pl', 'yourpassword')
        server.send_message(msg)

@router.post("/register")
def register_user(email: str, password: str, db: Session = Depends(get_db)):
    hashed_password = pwd_context.hash(password)
    user = User(email=email, hashed_password=hashed_password, is_verified=False)
    db.add(user)
    db.commit()
    db.refresh(user)
    
    send_verification_email(email, "some-generated-token")  # TODO: Dodać generowanie tokena
    
    return {"message": "Użytkownik zarejestrowany. Sprawdź e-mail, aby potwierdzić konto."}

@router.get("/verify/{token}")
def verify_user(token: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == "user-matching-token@example.com").first()  # TODO: Wyszukiwanie po tokenie
    if not user:
        raise HTTPException(status_code=404, detail="Nieprawidłowy token")
    
    user.is_verified = True
    db.commit()
    return {"message": "Konto zweryfikowane! Możesz się teraz zalogować."}
