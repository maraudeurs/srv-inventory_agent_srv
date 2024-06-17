from pydantic import BaseModel

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
    instance_memory: str
    instance_cpu: str
    update_date: str
    creation_date: str

class InstanceCreate(InstanceBase):
    pass

class Instance(InstanceBase):
    id: int

    class Config:
        orm_mode = True
