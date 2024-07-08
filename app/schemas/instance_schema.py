from pydantic import BaseModel
from datetime import date, datetime

class InstanceBase(BaseModel):
    name: str
    description: str
    ip_v4: str
    ip_v6: str
    status: str
    main_usage: str
    location: str
    tag: str
    cloud_model: str
    cloud_provider: str
    provider_uuid: str
    instance_memory: int
    instance_cpu: int
    in_bandwidth: str
    out_bandwidth: str
    cloud_service_type: str
    inventory_source_method: str
    system_os: str
    system_release: str
    system_architecture: str
    hostname: str
    python_version: str
    update_date: datetime
    creation_date: datetime

class InstanceCreate(InstanceBase):
    virtualization_method: list

class Instance(InstanceBase):
    id: int

    class Config:
        orm_mode = True
