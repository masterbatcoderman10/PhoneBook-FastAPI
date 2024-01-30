from typing import Annotated, Union
from datetime import datetime, timedelta, timezone
from sqlalchemy import select
from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter, HTTPException, Cookie, Response, Form
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, APIKeyCookie
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from ..migrations import User
from ..dependencies import engine
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 12

##Google Stuff
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserM(BaseModel):
    id: int
    username: str
    password: str
    verified: bool
    disabled: bool

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
cookie_scheme = APIKeyCookie(name="access_token", auto_error=True)

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)

def get_user(username: str):
    with Session(engine) as session:
        user = session.execute(select(User).where(User.username == username)).scalars().first()
        return UserM(id=user.id, username=user.username, password=user.password, verified=user.verified, disabled=user.disabled)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_hashed_password(password):
    return pwd_context.hash(password)

def authenticate_user(username: str, password: str):
    user = get_user(username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user

def authenticate_token(token: Annotated[str, Depends(cookie_scheme)]) -> TokenData:
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception 

    return token_data

#JWT token encodes the username and expiry time
#JWT token is signed with a secret key
#JWT token is returned to the user
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    data_to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=30)
    #Adding expiration time to the data that will be encoded in the JWT token
    data_to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(data_to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_tokens(username: str):
    access_token_expiry_duration = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expiry_duration = timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub" : username}, expires_delta=access_token_expiry_duration
    )
    refresh_token = create_access_token(
        data={"sub" : username}, expires_delta=refresh_token_expiry_duration
    )

    return access_token, refresh_token


#first-party authentication


#getting user profile
    #user sends the JWT token in the header
    #JWT token is decoded
    #JWT token is verified with the secret key
        #decoded details are verified with the database
    #user profile is returned to the user
async def get_current_user(token_data: Annotated[str, Depends(authenticate_token)]) -> UserM:
    
    user = get_user(username=token_data.username)
    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    return user

async def get_current_user_id(current_user: Annotated[UserM, Depends(get_current_user)]) -> int:
    return current_user.id

#user tries to logs in
#first username is checked in the database and hashed password is retrieved
#user password hash is matched with the password hash in the database
#if the password hash matches, then the user is given a JWT token and sent via 2 cookies, one for access token and one for refresh token
#if the password hash does not match, then the user is given an error message
@router.post("/token")
async def login_fp(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], response: Response):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )

    access_token, refresh_token = get_tokens(user.username)
    
    response.set_cookie(key="refresh_token", value=refresh_token, httponly=True)
    response.set_cookie(key="access_token", value=access_token, httponly=True)
    return {"message" : "Login successful"}

@router.post("/signup")
async def signup_fp(response: Response, username: str = Form(), password: str = Form()):
    with Session(engine) as session:
        user = session.execute(select(User).where(User.username == username)).scalars().first()
        if user:
            raise HTTPException(
                status_code=400,
                detail="Username already exists",
                headers={"WWW-Authenticate": "Bearer"}
            )
        if len(password) < 8:
            raise HTTPException(
                status_code=400,
                detail="Password must be at least 8 characters long",
                headers={"WWW-Authenticate": "Bearer"}
        )
        hashed_password = get_hashed_password(password)
        new_user = User(username=username, password=hashed_password, verified=True, disabled=False)
        session.add(new_user)
        session.commit()
    
    access_token, refresh_token = get_tokens(username)

    response.set_cookie(key="access_token", value=access_token, httponly=True)
    response.set_cookie(key="refresh_token", value=refresh_token, httponly=True)

    return {"message" : "Signup successful"}

@router.get("/me")
async def read_users_me(current_user: Annotated[UserM, Depends(get_current_user)]):
    return current_user