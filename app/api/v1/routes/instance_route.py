from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from typing import List

from app.models.instance_model import Instance as ORMInstance
from app.schemas.instance_schema import Instance, InstanceCreate
from app.services.instance_service import InstanceService
from app.auth.user_service import get_current_active_user
from app.schemas.user_schema import User
from app.auth.basic_auth_service import authenticate
from app.dependencies import get_db

router = APIRouter()
instance_service = InstanceService()

@router.get("/instances/", response_model=List[Instance])
def read_instances(db: Session = Depends(get_db), current_user: User= Depends(get_current_active_user)):
    instances = instance_service.get_instances(db)
    return instances

@router.post("/instances/", response_model=Instance)
def create_instance(instance_data: InstanceCreate, db: Session = Depends(get_db), credentials: HTTPBasicCredentials = Depends(authenticate)):
    """send instance to inventory server
    Args:
    - instance: instance object
    """
    instance = instance_service.create_instance(db, instance_data.dict())
    return instance