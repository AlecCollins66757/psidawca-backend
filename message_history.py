from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
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

class MessageHistory(Base):
    __tablename__ = "message_history"
    
    id = Column(Integer, primary_key=True, index=True)
    sender_name = Column(String, nullable=False)
    sender_email = Column(String, nullable=False)
    message = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    dog_id = Column(Integer, ForeignKey("dogs.id"))
    owner_id = Column(Integer, ForeignKey("users.id"))

@router.post("/contact/{dog_id}/save")
def save_message(dog_id: int, sender_name: str, sender_email: str, message: str, db: Session = Depends(get_db)):
    dog = db.query(Dog).filter(Dog.id == dog_id, Dog.is_active == True).first()
    if not dog:
        raise HTTPException(status_code=404, detail="Pies nie znaleziony lub nieaktywny")
    
    owner = db.query(User).filter(User.id == dog.owner_id).first()
    if not owner:
        raise HTTPException(status_code=404, detail="Właściciel nie znaleziony")
    
    new_message = MessageHistory(
        sender_name=sender_name,
        sender_email=sender_email,
        message=message,
        dog_id=dog.id,
        owner_id=owner.id
    )
    db.add(new_message)
    db.commit()
    return {"message": "Wiadomość zapisana w historii"}

@router.get("/admin/messages", response_model=List[dict])
def get_messages(user: User = Depends(read_users_me), db: Session = Depends(get_db)):
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Brak uprawnień administratora")
    
    messages = db.query(MessageHistory).all()
    return [{
        "id": msg.id,
        "sender_name": msg.sender_name,
        "sender_email": msg.sender_email,
        "message": msg.message,
        "timestamp": msg.timestamp,
        "dog_id": msg.dog_id,
        "owner_id": msg.owner_id
    } for msg in messages]
