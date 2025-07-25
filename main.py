from fastapi import FastAPI
from routers import contacts, users, google
from starlette.middleware.sessions import SessionMiddleware
import os
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")

app = FastAPI()

app.include_router(contacts.router)
app.include_router(users.router)
app.include_router(google.router)

app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)
#add SECRET_KEY to app config




@app.get("/")
async def root():
    return {"message": "This is the phonebook API"}