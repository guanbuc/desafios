# -*- encoding:utf-8 -*-


from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from models import Base
from sqlalchemy.pool import NullPool
import cx_Oracle as ora


dsn = """(DESCRIPTION = 
            (ADDRESS = (PROTOCOL = TCP)(HOST = 192.168.204.158)(PORT = 1521))
            (CONNECT_DATA = 
                (SERVER = DEDICATED)
                (SERVICE_NAME = bratus
            )
        )"""
#pool = ora.SessionPool(user='SYSTEM', password='000000', dsn=dsn, min=2, max=5, increment=1, threaded=True,
#                       encoding='UTF-8', nencoding='UTF-8')
#SQLALCHEMY_DATABASE_URI = 'oracle://'
#engine = create_engine(SQLALCHEMY_DATABASE_URI, creator=pool.acquire, poolclass=NullPool)
#engine = create_engine("oracle+cx_oracle://system:000000@192.168.204.158:1521/?service_name=bratus&encoding=UTF-8&nencoding=UTF-8")
engine = create_engine("oracle+cx_oracle://system:000000@192.168.56.105:1521/?service_name=bratus&encoding=UTF-8&nencoding=UTF-8")
db_session = scoped_session(sessionmaker(bind=engine))

Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)
Base.query = db_session.query_property()


def init_db():
    from models import Department, Employee, Role

    engineering = Department(id=1, name='Engineering')
    db_session.add(engineering)

    hr = Department(id=2, name='Human Resource')
    db_session.add(hr)

    manager = Role(role_id=2, name='manager')
    db_session.add(manager)

    engineer = Role(role_id=1, name='engineer')
    db_session.add(engineer)

    peter = Employee(id=1, name='Peter', dapartment_id=1, role_id=1)
    db_session.add(peter)
    roy = Employee(id=2, name='Roy', dapartment_id=1, role_id=1)
    db_session.add(roy)
    tracy = Employee(id=3, name='Tracy', dapartment_id=2, role_id=2)
    db_session.add(tracy)

    db_session.commit()