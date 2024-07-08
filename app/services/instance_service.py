from fastapi import HTTPException
from sqlalchemy.orm import Session
from typing import List
from fastapi.encoders import jsonable_encoder

from app.models.instance_model import Instance, VirtualizationMethod

class InstanceService:
    def get_instances(self, db: Session) -> List[Instance]:
        return db.query(Instance).all()

    def create_instance(self, db: Session, instance_data: dict) -> Instance:
        try:
            instance_in_db = db.query(Instance).filter(Instance.ip_v4 == instance_data['ip_v4']).first()
        except Exception as e:
            raise HTTPException(status_code=400, detail="cannot search instance in database")

        if instance_in_db:
            raise HTTPException(status_code=400, detail=f"Instance already registered {instance_data['ip_v4']}")

        try:
            ## pop virtualization_method
            db_instance_data = dict(instance_data)
            del db_instance_data['virtualization_method']
            db_instance = Instance(**db_instance_data)
            db.add(db_instance)
            db.commit()

            # Manage virtualization methods
            for virtualization_method in instance_data['virtualization_method']:
                virtualization_method_orm_object = VirtualizationMethod(instance_id=db_instance.id, name=virtualization_method)
                db.add(virtualization_method_orm_object)
            db.commit()
            db.refresh(db_instance)

        except Exception as e:
                db.rollback()
                return {"error": str(e)}, 400

        return db_instance

    def validate_instance_availability(self, instance: dict) -> Instance:
        """check instance availability """
        return instance