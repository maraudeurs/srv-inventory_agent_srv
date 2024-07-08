from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, Mapped, relationship, mapped_column
from typing import List

Base = declarative_base()

class Instance(Base):
    __tablename__ = 'instance'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
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
    instance_memory = Column(Integer)
    instance_cpu = Column(Integer)
    in_bandwidth = Column(String)
    out_bandwidth = Column(String)
    cloud_service_type = Column(String) ## public_cloud, private_cloud, baremetal
    inventory_source_method = Column(String) ## inventory_agent, cloud_api_provider
    system_os = Column(String)
    system_release = Column(String)
    system_architecture = Column(String)
    hostname = Column(String)
    python_version = Column(String)
    virtualization_method: Mapped[List["VirtualizationMethod"]] = relationship()
    update_date = Column(DateTime)
    creation_date = Column(DateTime)

class VirtualizationMethod(Base):
    __tablename__ = 'virtualization_method'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    instance_id: Mapped[int] = mapped_column(ForeignKey("instance.id"))
    name = Column(String, index=True)
    instance: Mapped["Instance"] = relationship(back_populates="virtualization_method")