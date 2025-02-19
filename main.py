from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Montowanie plików statycznych (CSS, JS)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Inicjalizacja systemu szablonów
templates = Jinja2Templates(directory="templates")

# Endpoint do renderowania formularza rejestracji psa
@app.get("/register_dog")
async def register_dog(request: Request):
    return templates.TemplateResponse("register_dog.html", {"request": request})
