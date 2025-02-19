from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey, Float
from sqlalchemy.orm import relationship
from database import Base
from sqlalchemy import Column, Integer, String, Float, Date
from sqlalchemy.orm import declarative_base, sessionmaker
from database import Base  # Upewnij się, że to jest poprawnie importowane!
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)  # Czy użytkownik potwierdził e-mail
    
    dogs = relationship("Dog", back_populates="owner")

class Dog(Base):
    __tablename__ = "dogs"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    chip_number = Column(String, unique=True, nullable=False)
    breed = Column(String, nullable=False)
    blood_type = Column(String, nullable=False)
    birth_date = Column(Date, nullable=False)
    weight = Column(Float, nullable=False)
    city = Column(String, nullable=False)
    region = Column(String, nullable=False)  # Województwo
    last_vaccination = Column(Date, nullable=False)
    is_active = Column(Boolean, default=True)  # Czy pies jest aktywny w bazie
    owner_id = Column(Integer, ForeignKey("users.id"))
    
    owner = relationship("User", back_populates="dogs")

# Dodanie pliku do obsługi bazy danych
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://user:password@localhost/psidawca"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

from sqlalchemy import Column, Integer, String, Float, Date
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Dog(Base):
    __tablename__ = "dogs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    chip_number = Column(String, unique=True, nullable=False)
    breed = Column(String, nullable=False)
    blood_type = Column(String, nullable=False)
    weight = Column(Float, nullable=False)
    birth_date = Column(Date, nullable=False)
    last_vaccination = Column(Date, nullable=False)
    city = Column(String, nullable=False)
    region = Column(String, nullable=False)

