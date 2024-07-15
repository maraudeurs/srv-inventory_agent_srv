

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Optional, Annotated
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.models.user_model import User as ORMUser
from app.schemas.user_schema import UserCreate, User
from app.schemas.token_schema import TokenData
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2bearer = OAuth2PasswordBearer(tokenUrl = 'v1/token')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def get_user(db, username: str,) -> Optional[ORMUser]:
    try:
        db_user = db.query(ORMUser).filter(ORMUser.username == username).first()
        return db_user
    except Exception as e:
        raise HTTPException(status_code=400, detail="cannot look for user in database")

def authenticate_user(db, username: str, password: str) -> Optional[ORMUser]:
    user = get_user(db, username)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user

# def create_user(db, user: UserCreate):
#     try:
#         db_user = db.query(ORMUser).filter(ORMUser.email == user.email).first()
#     except Exception as e:
#         raise HTTPException(status_code=400, detail="cannot search user in database")

#     if db_user:
#         raise HTTPException(status_code=400, detail="Email already registered")

#     hashed_password = get_password_hash(user.password)
#     db_user = ORMUser(username=user.username, email=user.email, hashed_password=hashed_password)
#     try:
#         db.add(db_user)
#         db.commit()
#         db.refresh(db_user)
#         return db_user
#     except Exception as e:
#         db.rollback()
#         raise HTTPException(status_code=400, detail="Error creating user")


async def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2bearer)):
    """
    Get current user from JWT token
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(db, token_data.username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: Annotated[ORMUser, Depends(get_current_user)]):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

