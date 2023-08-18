# -*- encoding:utf-8 -*-


from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Department(Base):
    __tablename__ = 'ORA_DEPARTMENT'
    id = Column(Integer, primary_key=True)
    name = Column(VARCHAR(100))


class Role(Base):
    __tablename__ = 'ORA_ROLE'
    role_id = Column(Integer, primary_key=True)
    name = Column(VARCHAR(100))


class Employee(Base):
    __tablename__ = 'ORA_EMPLOYEE'
    id = Column(Integer, primary_key=True)
    name = Column(VARCHAR(100))
    hired_on = Column(Date, default=func.now())
    dapartment_id = Column(Integer)
    role_id = Column(Integer)