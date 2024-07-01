from fastapi import APIRouter, Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from jose import JWTError, jwt
from typing import Annotated


from app.models.user_model import User as ORMUser
from app.schemas.user_schema import User, UserCreate
from app.schemas.token_schema import Token, TokenData
from app.dependencies import get_db
from app.auth.user_service import get_user, create_user, authenticate_user, get_current_active_user, oauth2bearer
from app.auth.token_service import create_access_token
from app.core.config import settings

router = APIRouter()

@router.post("/register", response_model=User)
def register_user(payload: UserCreate, db: Session = Depends(get_db)):
    if not payload.username:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Please add Username",
        )
    user = get_user(db, payload.username)
    if user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Email already registered",
        )
    user = create_user(db, payload)
    return user

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db))-> Token:
    """
    Login user based on email and password, then generate and return token
    """
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(token=token, token_type="bearer")

@router.get("/users/me/", response_model=User)
async def read_users_me(current_user: Annotated[User, Depends(get_current_active_user)]):
    return current_user