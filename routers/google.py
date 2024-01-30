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
from ..migrations import User
from ..dependencies import engine
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
async def auth(request: Request):
    print(request.session)
    try:
        token = await oauth.google.authorize_access_token(request)
        userinfo = token.get('userinfo')
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
async def logout(request: Request):
    # Delete the user's session
    request.session.clear()
    # Return a response indicating that the user has been logged out
    return {"detail": "Logged out"}

