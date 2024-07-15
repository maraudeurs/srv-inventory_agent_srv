from fastapi import HTTPException
from sqlalchemy.orm import Session
from typing import List
from fastapi.encoders import jsonable_encoder

from app.models.database_data_handler_utils import manage_instance_creation_date
from app.models.instance_model import Instance as InstanceORM, Ipv4 as Ipv4ORM, Ipv6 as Ipv6ORM, VirtualizationMethod as VirtualizationMethodORM
from app.schemas.instance_schema import Instance, InstanceCreate, Ipv4, Ipv6, VirtualizationMethod, VirtualizationMethodCreate
from app.dependencies import logger

class InstanceService:
    def get_instances(self, db: Session) -> List[InstanceORM]:
        return db.query(InstanceORM).all()

    def create_instance(self, db: Session, instance_data: InstanceCreate) -> Instance:
        instance_in_db = db.query(InstanceORM).filter(InstanceORM.main_ipv4 == instance_data.main_ipv4).first()
        if instance_in_db:
            logger.debug(f"Instance with ipv4 address :{instance_data.main_ipv4} already exist in database")
            raise HTTPException(status_code=400, detail=f"Instance already registered {instance_data.main_ipv4}")
        try:
            ## instance does not exist then update data accordingly
            db_instance_data = manage_instance_creation_date(db, instance_data)

            db_instance = InstanceORM(
                name=instance_data.name,
                description=instance_data.description,
                main_ipv4=instance_data.main_ipv4,
                status=instance_data.status,
                main_group=instance_data.main_group,
                environment=instance_data.environment,
                ansible_ssh_user=instance_data.ansible_ssh_user,
                main_usage=instance_data.main_usage,
                location=instance_data.location,
                tag=instance_data.tag,
                cloud_model=instance_data.cloud_model,
                cloud_provider=instance_data.cloud_provider,
                provider_uuid=instance_data.provider_uuid,
                instance_memory=instance_data.instance_memory,
                instance_cpu=instance_data.instance_cpu,
                in_bandwidth=instance_data.in_bandwidth,
                out_bandwidth=instance_data.out_bandwidth,
                cloud_service_type=instance_data.cloud_service_type,
                inventory_source_method=instance_data.inventory_source_method,
                system_os=instance_data.system_os,
                system_release=instance_data.system_release,
                system_architecture=instance_data.system_architecture,
                hostname=instance_data.hostname,
                python_version=instance_data.python_version,
                update_date=instance_data.update_date,
                creation_date=instance_data.creation_date,
            )


            # Create or get virtualization methods and associate them with the instance
            for method in instance_data.virtualization_method:
                db_method = db.query(VirtualizationMethodORM).filter(VirtualizationMethodORM.name == method).first()
                if db_method is None:
                    db_method = VirtualizationMethodORM(name=method)
                    db.add(db_method)
                db_instance.virtualization_method.append(db_method)


            db.add(db_instance)
            db.commit()

            ## Manage ipv4 list
            for ipv4_address in instance_data.ip_v4_list:
                ipv4_address_orm_object = Ipv4ORM(instance_id=db_instance.id, ip=ipv4_address)
                db.add(ipv4_address_orm_object)
            db.commit()

            ## Manage ipv6 list
            for ipv6_address in instance_data.ip_v6_list:
                ipv6_address_orm_object = Ipv6ORM(instance_id=db_instance.id, ip=ipv6_address)
                db.add(ipv6_address_orm_object)
            db.commit()

            ## add instance to db
            db.refresh(db_instance)
            logger.info(f"Instance with ipv4 address : {instance_data.main_ipv4} successfully registered")

            return db_instance

        except Exception as e:
                db.rollback()
                return {"error": str(e)}, 400


    def validate_instance_availability(self, instance: Instance) -> Instance:
        """check instance availability """
        return instance