from fastapi import APIRouter
from pydantic import BaseModel

class Contact(BaseModel):
    id: int
    name: str
    phone: str
    age: int

router = APIRouter(
    prefix="/contacts",
    tags=["contacts"],
    responses={404: {"description": "Not found"}},
)

@router.get("/{contact_id}")
async def get_contact(contact_id: int) -> Contact:
    #have to add JWT authentication
    return {"id": contact_id, "name": "John Doe", "phone": "555-555-5555", "age": 30}

@router.get("/")
async def get_contacts() -> list[Contact]:
    #have to add JWT authentication
    return [
        {"id": 1,"name": "John Doe", "phone": "555-555-5555", "age": 30},
    ]

@router.post("/")
async def add_contact(contact: Contact):
    #have to add JWT authentication
    return contact