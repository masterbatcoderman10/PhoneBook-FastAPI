from typing import Annotated, Union
from datetime import datetime, timedelta, timezone
from sqlalchemy import select
from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter, HTTPException, Cookie, Response, Form, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, APIKeyCookie
from fastapi.responses import RedirectResponse
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from migrations import User
from dependencies import engine
from .users import get_tokens, ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_MINUTES
import os
from dotenv import load_dotenv
from starlette.config import Config
from authlib.integrations.starlette_client import OAuth, OAuthError

##Google Stuff
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

config_data = {
    "GOOGLE_CLIENT_ID" : GOOGLE_CLIENT_ID,
    "GOOGLE_CLIENT_SECRET" : GOOGLE_CLIENT_SECRET,
}

starlette_config = Config(environ=config_data)
oauth = OAuth(starlette_config)
oauth.register(
    name="google",
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={
        'scope': 'openid email profile'
    }
)

router = APIRouter(
    prefix="/google",
    tags=["google"],
    responses={404: {"description": "Not found"}},
)

@router.get("/login")
async def login_google(request: Request):
    request.session.clear()
    redirect_uri = request.url_for('auth')
    try:
        auth_url = await oauth.google.authorize_redirect(request, redirect_uri)
        return auth_url

    except OAuthError as e:
        print(e)
        return HTTPException(
            status_code=400,
            detail="State mismatch",
        )
    

@router.get("/auth")
async def auth(request: Request, response: Response):
    print(request.session)
    try:
        token = await oauth.google.authorize_access_token(request)
        userinfo = token.get('userinfo')
        #check if user exists in db if they don't add them
        with Session(engine) as session:
            user = session.execute(select(User).where(User.username == userinfo['email'])).scalars().first()
            if user is None:
                #create user
                user = User(username=userinfo['email'], password="none", verified=True, disabled=False)
                session.add(user)
                session.commit()

        access_token, refresh_token = get_tokens(userinfo['email'])
        response.set_cookie(key="access_token", value=access_token, httponly=True)
        response.set_cookie(key="refresh_token", value=refresh_token, httponly=True)

        return {"message" : "Signup successful"}




        request.session.pop('_state_google_' + request.query_params['state'], None)
    except OAuthError as e:
        print(e)
        return HTTPException(
            status_code=400,
            detail="State mismatch",
        )
    # except Exception as e:
    #     print(e)
    #     return HTTPException(
    #         status_code=400,
    #         detail="Some error",
    #     )
    return userinfo


@router.get("/logout")
async def logout(request: Request, response: Response):
    # Delete the user's session
    request.session.clear()
    # Delete the user's cookies
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    # Return a response indicating that the user has been logged out
    return {"detail": "Logged out"}

