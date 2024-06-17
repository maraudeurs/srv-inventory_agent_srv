from sqlalchemy.orm import Session
from typing import List
from app.models.instance_model import Instance

class InstanceService:
    def get_instances(self, db: Session) -> List[Instance]:
        return db.query(Instance).all()

    def create_instance(self, db: Session, instance_data: dict) -> Instance:
        # existing_instance = instances_collection.find_one({"instance_id": instance.instance_id})
        # if existing_instance:
        #     raise ValueError("Instance with ID {} already exists".format(instance.instance_id))
        db_instance = Instance(**instance_data)
        db.add(db_instance)
        db.commit()
        db.refresh(db_instance)
        return db_instance

    def validate_instance_availability(self, instance: dict) -> Instance:
        """check instance availability """
        return instance