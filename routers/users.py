from typing import Annotated

from fastapi import Depends, APIRouter, HTTPException
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from ..migrations import User

class UserM(BaseModel):
    id: int
    username: str
    password: str

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

mock_users_db = [
    {
        "id" : 1, 
        "username" : "John Doe",
        "password" : "password"
    }
]

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)

#first-party authentication
#user logs in
    #user password hash is matched with the password hash in the database
    #if the password hash matches, then the user is given a JWT token
        #JWT token encodes the user's id and username
        #JWT token is signed with a secret key
        #JWT token is returned to the user
    #if the password hash does not match, then the user is given an error message

#getting user profile
    #user sends the JWT token in the header
    #JWT token is decoded
    #JWT token is verified with the secret key
        #decoded details are verified with the database
    #user profile is returned to the user

def decode_and_verify(token: str):
    pass

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    pass

@router.get("/me")
async def read_users_me(current_user: Annotated[UserM, Depends(get_current_user)]):
    return current_user