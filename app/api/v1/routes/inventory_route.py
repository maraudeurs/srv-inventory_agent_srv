from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from typing import List

# from app.models.instance_model import Instance as ORMInstance
# from app.schemas.instance_schema import Instance, InstanceCreate
from app.services.inventory_service import InventoryService
from app.auth.user_service import get_current_active_user
from app.schemas.user_schema import User
from app.auth.basic_auth_service import authenticate
from app.dependencies import get_db

router = APIRouter()
inventory_service = InventoryService()

@router.get("/inventory/")
def get_inventory(db: Session = Depends(get_db), current_user: User= Depends(get_current_active_user)):
    """
    Route to generate inventory from instance in database

    Args:
        db : SQLAlchemy session object
        current_user : user object from authentication (get_current_active_user)

    Returns:
        str : command output result or None if error
    """
    inventory = inventory_service.generate_inventory(db)
    return inventory

# @router.post("/instances/", response_model=Instance)
# def create_instance(instance_data: InstanceCreate, db: Session = Depends(get_db), credentials: HTTPBasicCredentials = Depends(authenticate)):
#     """
#     Create instance in inventory server database

#     Args:
#         instance: instance object
#     """

#     instance = instance_service.create_instance(db, instance_data)
#     return instance
