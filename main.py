from fastapi import FastAPI
from .routers import contacts, users

app = FastAPI()

app.include_router(contacts.router)
app.include_router(users.router)


@app.get("/")
async def root():
    return {"message": "This is the phonebook API"}