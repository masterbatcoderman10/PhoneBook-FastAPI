from fastapi import APIRouter
from fastapi.security import OAuth2PasswordBearer
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

##Google Stuff
GOOGLE_CLIENT_ID = "714972680282-kbtuq4set57loh9l97a2s406e7ki1cgd.apps.googleusercontent.com"
GOOGLE_CLIENT_SECRET = "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"


#http://localhost/token is where the user should use to get the token.abs
#This token will be generated during signin and will be used to authenticate the user later on.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

mock_contacts = [
        {"id": 1,"name": "John Doe", "phone": "555-555-5555", "age": 30},
    ]

@router.get("/")
async def get_contacts() -> list[Contact]:
    #have to add JWT authentication
    return mock_contacts

@router.get("/{contact_id}")
async def get_contact(contact_id: int) -> Contact:
    #have to add JWT authentication
    return mock_contacts[contact_id]


@router.post("/")
async def add_contact(contact: Contact):
    #have to add JWT authentication
    return contact