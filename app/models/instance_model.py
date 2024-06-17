from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Instance(Base):
    __tablename__ = 'instances'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, index=True)
    description = Column(String)
    ip_v4 = Column(String)
    ip_v6 = Column(String)
    status = Column(String)
    main_usage = Column(String)
    location = Column(String)
    tag = Column(String)
    cloud_model = Column(String)
    cloud_provider = Column(String)
    provider_uuid = Column(String)
    instance_memory = Column(String)
    instance_cpu = Column(String)
    update_date = Column(String)
    creation_date = Column(String)