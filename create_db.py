from sqlalchemy import create_engine
from database import Base

# Pobierz dane do bazy z ustawień aplikacji
DATABASE_URL = "postgresql://psidawca_db_user:1H1GEy4rzch0EkFcwVYIoRpdRBXlUN0x@dpg-cuqdkpij1k6c73e038dg-a.oregon-postgres.render.com/psidawca_db"

engine = create_engine(DATABASE_URL)

# Tworzenie tabel
Base.metadata.create_all(engine)

print("✅ Baza danych i tabele zostały utworzone!")
