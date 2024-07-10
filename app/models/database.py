import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.core.config import settings

from app.core.security import get_password_hash

DATABASE_URL = settings.database_url
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db(engine):
    from app.models.instance_model import Instance
    from app.models.user_model import User
    logging.info("Initializing the database.")
    Instance.metadata.create_all(bind=engine)
    User.metadata.create_all(bind=engine)

    ## create user based on config
    db = Session(bind=engine)
    user = db.query(User).filter(User.username == settings.admin_username).first()
    if not user:
        user = User(
            username=settings.admin_username,
            email=settings.admin_email,
            hashed_password=get_password_hash(settings.admin_password),
            disabled=False
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    db.close()

def purge_db(engine):
    from app.models.instance_model import Instance
    from app.models.user_model import User
    logging.info("purging database.")
    Instance.metadata.drop_all(bind=engine)
    User.metadata.drop_all(bind=engine)