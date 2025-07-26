from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import contacts, users, google
from starlette.middleware.sessions import SessionMiddleware
import os
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8000",
        "http://127.0.0.1:8000"
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

app.include_router(contacts.router)
app.include_router(users.router)
app.include_router(google.router)

app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)
#add SECRET_KEY to app config




@app.get("/")
async def root():
    return {"message": "This is the phonebook API"}