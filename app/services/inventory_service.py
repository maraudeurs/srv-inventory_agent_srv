from fastapi import HTTPException
from sqlalchemy.orm import Session
from typing import List
from fastapi.encoders import jsonable_encoder

from app.models.instance_model import Instance as InstanceORM
from app.dependencies import logger


class InventoryService:
    """
    Get all instances from database

    Args:
        db : SQLAlchemy Session object

    Returns:
        list: list of instanceORM object
    """
    def get_instances(self, db: Session) -> List[InstanceORM]:
        try:
            hosts = db.query(InstanceORM).all()
            return hosts
        finally:
            db.close()


    def generate_inventory(self, db: Session) -> dict:
        """
        Generate ansible inventory based on instance data

        Returns:
            dict : ansible inventory as python dict
        """
        hosts = self.get_instances(db)
        inventory = {"all": {"hosts": {}, "children": {}}}

        for host in hosts:
            host_name = host.name
            host_ip = host.main_ipv4
            host_group = host.main_group
            if host_group:
                if host_group not in inventory["all"]["children"]:
                    inventory["all"]["children"][host_group] = {"hosts": {}}
                inventory["all"]["children"][host_group]["hosts"][host_name] = {"ansible_host": host_ip}
            else:
                inventory["all"]["hosts"][host_name] = {"ansible_host": host_ip}

        return inventory