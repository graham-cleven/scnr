#! /usr/bin/env python3


from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Users(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True)
    username = Column(String(256), unique=True)
    first_name = Column(String(32))
    last_name = Column(String(32))
    pw_hash = Column(String(256))
    rbac_role = Column(String(32))


class Roles(Base):
    __tablename__ = "roles"
    role_id = Column(Integer, primary_key=True)
    role_name = Column(String(32), unique=True)
    role_ldap = Column(String(64), unique=True)
    role_perms = Column(String(1024))


class Perms(Base):
    __tablename__ = "perms"
    perm_id = Column(Integer, primary_key=True)
    perm_name = Column(String(32), unique=True)


class Jobs(Base):
    __tablename__ = "jobs"
    job_id = Column(Integer, primary_key=True)
    job_creator = Column(Integer)
    job_status = Column(Integer, default=1)
    job_query = Column(String(1024), default=None)
    job_type = Column(String(32), default="manual") # "nlp", "manual"


class Responses(Base):
    __tablename__ = "responses"
    response_id = Column(Integer, primary_key=True)
    response_status = Column(Integer, default=0)
    job_id = Column(Integer())
    job_cmd_line = Column(String(1024))
    box_id = Column(Integer)
    response_status = Column(Integer())
    response_output = Column(Text(64000))  # txt, blob?


class Boxes(Base):
    __tablename__ = "boxes"
    box_id = Column(Integer, primary_key=True)
    box_os = Column(String(32))
    box_os_cat = Column(String(32))
    box_pac_man = Column(String(32))
    box_pacs = Column(String(2048))
    box_kbs = Column(String(2048))
    box_ip = Column(String(1024))
    box_subnet = Column(String(64))
    box_hostname = Column(String(1024))
    box_last_contact = Column(String(64))
    box_proto = Column(String(64))
    box_port = Column(String(32))


class Settings(Base):
    __tablename__ = "settings"
    setting_id = Column(Integer, primary_key=True)
    setting_name = Column(String(64))
    setting_value = Column(String(128))
