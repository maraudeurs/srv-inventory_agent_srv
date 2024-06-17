import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

DATABASE_URL = settings.database_url

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    from app.models.instance_model import Instance
    from app.models.user_model import User
    logging.info("Initializing the database.")
    Instance.metadata.create_all(bind=engine)
    User.metadata.create_all(bind=engine)

def purge_db():
    from app.models.instance_model import Instance
    from app.models.user_model import User
    logging.info("purging database.")
    Instance.metadata.drop_all(bind=engine)
    User.metadata.drop_all(bind=engine)