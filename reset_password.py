from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext
import smtplib
from email.message import EmailMessage
import jwt
from datetime import datetime, timedelta

from database import SessionLocal
from models import User

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
RESET_TOKEN_EXPIRE_MINUTES = 15

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def send_reset_email(email: str, token: str):
    msg = EmailMessage()
    msg['Subject'] = 'Reset hasła'
    msg['From'] = 'kontakt@psidawca.pl'
    msg['To'] = email
    msg.set_content(f"Kliknij w link, aby zresetować hasło: https://psidawca.pl/reset/{token}")
    
    with smtplib.SMTP('smtp.yourmailserver.com', 587) as server:
        server.starttls()
        server.login('kontakt@psidawca.pl', 'yourpassword')
        server.send_message(msg)

def create_reset_token(email: str):
    expire = datetime.utcnow() + timedelta(minutes=RESET_TOKEN_EXPIRE_MINUTES)
    return jwt.encode({"sub": email, "exp": expire}, SECRET_KEY, algorithm=ALGORITHM)

@router.post("/forgot-password")
def forgot_password(email: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="Użytkownik nie znaleziony")
    
    reset_token = create_reset_token(user.email)
    send_reset_email(user.email, reset_token)
    return {"message": "E-mail z linkiem resetującym został wysłany."}

@router.post("/reset-password")
def reset_password(token: str, new_password: str, db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Nieprawidłowy token")
        user = db.query(User).filter(User.email == email).first()
        if user is None:
            raise HTTPException(status_code=404, detail="Użytkownik nie znaleziony")
        
        user.hashed_password = pwd_context.hash(new_password)
        db.commit()
        return {"message": "Hasło zostało zmienione."}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token wygasł")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Nieprawidłowy token")
