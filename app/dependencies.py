from sqlalchemy.orm import Session
from app.models.database import SessionLocal
from fastapi import Depends

## database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

