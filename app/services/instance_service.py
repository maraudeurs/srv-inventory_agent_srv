from fastapi import HTTPException
from sqlalchemy.orm import Session
from typing import List
from fastapi.encoders import jsonable_encoder

from app.models.database_data_handler_utils import manage_instance_creation_date
from app.models.instance_model import Instance as InstanceORM, Ipv4 as Ipv4ORM, Ipv6 as Ipv6ORM, VirtualizationMethod as VirtualizationMethodORM
from app.schemas.instance_schema import Instance, InstanceCreate, Ipv4, Ipv6, Virtualization_method

class InstanceService:
    def get_instances(self, db: Session) -> List[InstanceORM]:
        return db.query(InstanceORM).all()

    def create_instance(self, db: Session, instance_data: InstanceCreate) -> Instance:
        instance_in_db = db.query(InstanceORM).filter(InstanceORM.main_ipv4 == instance_data.main_ipv4).first()
        if instance_in_db:
            raise HTTPException(status_code=400, detail=f"Instance already registered {instance_data.main_ipv4}")
        try:
            ## instance does not exist then update data accordingly
            db_instance_data = manage_instance_creation_date(db, instance_data)

            db_instance = InstanceORM(
                name=instance_data.name,
                description=instance_data.description,
                main_ipv4=instance_data.main_ipv4,
                status=instance_data.status,
                # instance_memory=instance_data.instance_memory,
                # instance_cpu=instance_data.instance_cpu,
                inventory_source_method=instance_data.inventory_source_method,
                system_os=instance_data.system_os,
                system_release=instance_data.system_release,
                system_architecture=instance_data.system_architecture,
                hostname=instance_data.hostname,
                python_version=instance_data.python_version,
                update_date=instance_data.update_date,
                creation_date=instance_data.creation_date
            )

            # ## Manage ipv4 list
            # for ipv4_address in instance_data.ip_v4_list:
            #     db_instance.ip_v4_list.append(Ipv4ORM(ip=ipv4_address))
            # ## Manage ipv6 list
            # for ipv6_address in instance_data.ip_v6_list:
            #     db_instance.ip_v6_list.append(Ipv6ORM(ip=ipv6_address))

            db.add(db_instance)
            db.commit()
            db.refresh(db_instance)

            ## Manage virtualization methods
            for virtualization_method in instance_data.virtualization_method:
                virtualization_method_orm_object = VirtualizationMethodORM(instance_id=db_instance.id, name=virtualization_method)
                db.add(virtualization_method_orm_object)
            db.commit()
            db.refresh(db_instance)

            ## Manage ipv4 list
            for ipv4_address in instance_data.ip_v4_list:
                ipv4_address_orm_object = Ipv4ORM(instance_id=db_instance.id, ip=ipv4_address)
                db.add(ipv4_address_orm_object)
            db.commit()
            db.refresh(db_instance)

            ## Manage ipv6 list
            for ipv6_address in instance_data.ip_v6_list:
                ipv6_address_orm_object = Ipv6ORM(instance_id=db_instance.id, ip=ipv6_address)
                db.add(ipv6_address_orm_object)
            db.commit()
            db.refresh(db_instance)

        except Exception as e:
                db.rollback()
                return {"error": str(e)}, 400

        return Instance.from_orm(db_instance)

    def validate_instance_availability(self, instance: Instance) -> Instance:
        """check instance availability """
        return instance