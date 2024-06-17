# from fastapi import APIRouter, Depends, FastAPI, HTTPException, status
# from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
# from sqlalchemy.orm import Session
# # from datetime import datetime, timedelta
# # from jose import JWTError, jwt

# from app.models.user_model import User as ORMUser
# from app.schemas.user_schema import User, UserCreate, Token
# from app.services.user_service import UserService
# from app.dependencies import get_db

# router = APIRouter()
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token/")

# @router.post("/token/", response_model=Token)
# def login_for_access_token(db: Session = Depends(get_db),form_data: OAuth2PasswordRequestForm = Depends()):
#     user_service = UserService(db)
#     user = user_service.authenticate_user(form_data.username, form_data.password)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect username or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     access_token = user_service.create_access_token(data={"sub": user.username})
#     return {"access_token": access_token, "token_type": "bearer"}