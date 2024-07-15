from pydantic import BaseModel, field_serializer
from typing import Optional, List
from datetime import date, datetime
from app.core.config import settings

## ipv4 relation
class Ipv4Base(BaseModel):
    ip: str

class Ipv4Create(Ipv4Base):
    pass

class Ipv4(Ipv4Base):
    id: int
    instance_id: int

    class Config:
        orm_mode = True

## ipv6 relation
class Ipv6Base(BaseModel):
    ip: str

class Ipv6Create(Ipv6Base):
    pass

class Ipv6(Ipv6Base):
    id: int
    instance_id: int

    class Config:
        orm_mode = True

## virtualization_method relation
class VirtualizationMethodBase(BaseModel):
    name: str

class VirtualizationMethodCreate(VirtualizationMethodBase):
    pass

class VirtualizationMethod(VirtualizationMethodBase):
    id: int


    class Config:
        orm_mode = True

## instance schema
class InstanceBase(BaseModel):
    name: str
    description: Optional[str] = None
    main_ipv4 : Optional[str] = None
    status: str
    main_group: Optional[str] = None
    environment: Optional[str] = None
    ansible_ssh_user: Optional[str] = str(settings.default_ssh_user)
    main_usage: Optional[str] = None
    location: Optional[str] = None
    tag: Optional[str] = None
    cloud_model: Optional[str] = None
    cloud_provider: Optional[str] = None
    provider_uuid: Optional[str] = None
    instance_memory: Optional[int] = None
    instance_cpu: Optional[int] = None
    in_bandwidth: Optional[str] = None
    out_bandwidth: Optional[str] = None
    cloud_service_type: Optional[str] = None
    inventory_source_method: str
    system_os: Optional[str] = None
    system_release: Optional[str] = None
    system_architecture: Optional[str] = None
    hostname: Optional[str] = None
    python_version: Optional[str] = None

    update_date: datetime
    creation_date: datetime = None

    class Config:
        ## Allows Pydantic to serialize/deserialize SQLAlchemy models
        orm_mode = True
        from_attributes=True

class InstanceCreate(InstanceBase):
    virtualization_method: List[str]
    ip_v4_list: Optional[List[str]] = None
    ip_v6_list: Optional[List[str]] = None

class Instance(InstanceBase):
    id: int
    virtualization_method: List[VirtualizationMethod]
    ip_v4_list: Optional[List[Ipv4]]
    ip_v6_list: Optional[List[Ipv6]]




