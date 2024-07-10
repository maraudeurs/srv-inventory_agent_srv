import logging
import sys

from sqlalchemy.orm import Session
from app.models.database import SessionLocal
from fastapi import Depends
from app.core.config import settings

## database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


## logging dependency
def setup_logging(log_level, log_output, log_file):

    if log_output == "file":
        logging.basicConfig(
            filename=log_file,
            level=log_level,
            format="%(asctime)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
    else:
        logging.basicConfig(
            stream=sys.stdout,
            level=log_level,
            format="%(asctime)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

## Manage logging
setup_logging(settings.log_level, settings.log_output, settings.log_file)
logger = logging.getLogger(__name__)