from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, Mapped, relationship, mapped_column
from typing import List

Base = declarative_base()

class Instance(Base):
    __tablename__ = 'instance'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, index=True)
    description = Column(String)
    main_ipv4 = Column(String, nullable=True)
    ip_v4_list: Mapped[List["Ipv4"]] = relationship("Ipv4", back_populates="instance", cascade="all, delete-orphan")
    # ip_v4_list = relationship("Ipv4", back_populates="instance", cascade="all, delete-orphan")
    ip_v6_list: Mapped[List["Ipv6"]] = relationship("Ipv6", back_populates="instance", cascade="all, delete-orphan")
    # ip_v6_list = relationship("Ipv6", back_populates="instance", cascade="all, delete-orphan")
    status = Column(String)
    main_usage = Column(String, nullable=True)
    location = Column(String, nullable=True)
    tag = Column(String, nullable=True)
    cloud_model = Column(String, nullable=True)
    cloud_provider = Column(String, nullable=True)
    provider_uuid = Column(String, nullable=True)
    instance_memory = Column(Integer, nullable=True)
    instance_cpu = Column(Integer, nullable=True)
    in_bandwidth = Column(String, nullable=True)
    out_bandwidth = Column(String, nullable=True)
    cloud_service_type = Column(String, nullable=True) ## public_cloud, private_cloud, baremetal
    inventory_source_method = Column(String) ## inventory_agent, cloud_api_provider
    system_os = Column(String, nullable=True)
    system_release = Column(String, nullable=True)
    system_architecture = Column(String, nullable=True)
    hostname = Column(String)
    python_version = Column(String, nullable=True)
    virtualization_method: Mapped[List["VirtualizationMethod"]] = relationship()
    update_date = Column(DateTime)
    creation_date = Column(DateTime)

class VirtualizationMethod(Base):
    __tablename__ = 'virtualization_method'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, index=True)
    instance: Mapped["Instance"] = relationship(back_populates="virtualization_method")
    instance_id: Mapped[int] = mapped_column(ForeignKey("instance.id"))


class Ipv4(Base):
    __tablename__ = 'ipv4'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    ip = Column(String, index=True)
    instance_id: Mapped[int] = mapped_column(ForeignKey("instance.id"))
    instance: Mapped["Instance"] = relationship(back_populates="ip_v4_list")
    # instance = relationship("Instance", back_populates="ip_v4_list")
    # instance_id = Column(Integer, ForeignKey('instance.id'))

class Ipv6(Base):
    __tablename__ = 'ipv6'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    ip = Column(String, index=True)
    instance_id: Mapped[int] = mapped_column(ForeignKey("instance.id"))
    instance: Mapped["Instance"] = relationship(back_populates="ip_v6_list")
    # instance = relationship("Instance", back_populates="ip_v6_list")
    # instance_id = Column(Integer, ForeignKey('instance.id'))