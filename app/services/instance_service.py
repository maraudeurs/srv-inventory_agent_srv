from fastapi import HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.models.instance_model import Instance

class InstanceService:
    def get_instances(self, db: Session) -> List[Instance]:
        return db.query(Instance).all()

    def create_instance(self, db: Session, instance_data: dict) -> Instance:
        try:
            instance_in_db = db.query(Instance).filter(Instance.name == instance_data['name']).first()
        except Exception as e:
            raise HTTPException(status_code=400, detail="cannot search instance in database")

        if instance_in_db:
            raise HTTPException(status_code=400, detail="Instance already registered")

        db_instance = Instance(**instance_data)
        db.add(db_instance)
        db.commit()
        db.refresh(db_instance)
        return db_instance

    def validate_instance_availability(self, instance: dict) -> Instance:
        """check instance availability """
        return instance