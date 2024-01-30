from typing import Annotated, Union
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, APIKeyCookie
from pydantic import BaseModel
from .users import get_current_user_id
from ..migrations import User
from ..migrations import Contact
from ..dependencies import engine
from sqlalchemy import select
from sqlalchemy.orm import Session

class ContactM(BaseModel):
    id : int
    name: str
    phone: str
    age: int

router = APIRouter(
    prefix="/contacts",
    tags=["contacts"],
    responses={404: {"description": "Not found"}},
)

##Google Stuff
GOOGLE_CLIENT_ID = "714972680282-kbtuq4set57loh9l97a2s406e7ki1cgd.apps.googleusercontent.com"
GOOGLE_CLIENT_SECRET = "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"


#http://localhost/token is where the user should use to get the token.abs
#This token will be generated during signin and will be used to authenticate the user later on.

@router.get("/")
async def get_contacts(user_id : Annotated[int, Depends(get_current_user_id)]) -> list[ContactM]:
    #have to add JWT authentication
    with Session(engine) as session:
        contacts = session.execute(select(Contact).where(Contact.user_id == user_id)).scalars().all()
        map(lambda contact : ContactM(id=contact.id, name=contact.name, phone=contact.phone, age=contact.age), contacts)
    return contacts


@router.get("/{contact_id}")
async def get_contact(user_id : Annotated[int, Depends(get_current_user_id)], contact_id: int) -> ContactM:
    #have to add JWT authentication
    with Session(engine) as session:
        contact = session.execute(select(Contact).where(Contact.user_id == user_id and Contact.id == contact_id)).scalars().first()
    return ContactM(name=contact.name, phone=contact.phone, age=contact.age)


@router.post("/")
async def add_contact(user_id : Annotated[int, Depends(get_current_user_id)], contact: ContactM):
    #have to add JWT authentication
    with Session(engine) as session:
        session.add(Contact(user_id=user_id, name=contact.name, phone=contact.phone, age=contact.age))
        session.commit()
    return {"message": "Contact added successfully"}