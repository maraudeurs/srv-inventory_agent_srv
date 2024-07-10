from datetime import datetime
from sqlalchemy.orm import Session
from app.models.instance_model import Instance
from app.schemas.instance_schema import InstanceCreate

def manage_instance_creation_date(db: Session, db_instance_data: InstanceCreate) -> InstanceCreate:
    """
    Manage instance creation date (set creation_date if newly registered instance)

    Args:
        db : database session
        db_instance_data : instance data as InstanceCreate schema

    Returns:
        dict: db_instance_data dict with creation_date field
    """

    # ## search if instance already exist in database
    # db.query(Instance).filter(Instance.provider_uuid == instance_id).first()
    # provider_uuid_query = Instance.select().where(Instance.columns.provider_uuid == instance_id)
    now = datetime.now()
    db_instance_data.creation_date = now
    return db_instance_data

def manage_instance_tag(db, instance_id) -> str:
    """
    Manage instance tag (if fisrt add, set tag to null, else keep existing tag)

    Args:
        db : database session
        instance_id : provider instance_id

    Returns:
        str: instance_tag
    """

    ## search instance
    # db.query(Instance).filter(Instance.provider_uuid == instance_id).first()