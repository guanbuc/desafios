# -*- encoding: utf-8 -*-


from sqlalchemy import *
from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

engine = create_engine('sqlite:////home/bratus/workspace/python-projects/desafios/ag_capital/database.db')

Base = declarative_base()

class Clientes(Base):
    __tablename__ = 'Clientes'

    Id = Column(Integer, primary_key=True)
    Name = Column(String, unique=True)

class Projetos(Base):
    __tablename__ = 'Projetos'

    Id = Column(Integer, primary_key=True)
    Name = Column(String, unique=True)
    ClientesId = Column(Integer ,unique=False)
    DataInicio = Column(Date, unique=False)
    DataFim = Column(Date, unique=False)

class Atividades(Base):
    __tablename__ = 'Atividades'

    Id = Column(Integer, primary_key=True)
    Descricao = Column(String, unique=False)
    ProjetosId = Column(Integer, unique=False)


class Database():
    Session = sessionmaker(bind=engine, autocommit=False)
    def __init__(self):
        self.session = self.Session()

    def DdlExecute(self):
        Base.metadata.create_all(engine)

    def DmlExecute(self, parametros=None):
        dql = 'select count(*) from Clientes'
        result = self.session.execute(dql)
        result = (list(result)[0])[0]

        if result == 0:
            dml = insert(Clientes).values(Id=1, Name=parametros[0]['cliente'])
            self.session.execute(dml)
            self.session.commit()

        else:
            dql = 'select max(Id) from Clientes'
            result = self.session.execute(dql)
            result = (list(result)[0])[0]

            dml = insert(Clientes).values(Id=result+1, Name=parametros[0]['cliente'])

            try:
                self.session.execute(dml)
                self.session.commit()
            except:
                pass

        dql = 'select count(*) from Projetos'
        result = self.session.execute(dql)
        result = (list(result)[0])[0]

        if result == 0:
            dql = select(Clientes.Id).where(Clientes.Name==parametros[0]['cliente'])
            result = self.session.execute(dql)
            result = (list(result)[0])[0]

            dml = insert(Projetos).values(Id=1, Name=parametros[0]['projeto'], \
                                          ClientesId=result, \
                                          DataInicio=datetime.strptime(parametros[0]['dtinicio'], '%d/%m/%Y'), \
                                          DataFim=datetime.strptime(parametros[0]['dtfim'], '%d/%m/%Y'))

            self.session.execute(dml)
            self.session.commit()

        else:
            dql = 'select max(Id) from Projetos'
            result = self.session.execute(dql)
            result = (list(result)[0])[0]

            dql = select(Clientes.Id).where(Clientes.Name==parametros[0]['cliente'])
            resultNw = self.session.execute(dql)
            resultNw = (list(resultNw)[0])[0]

            dml = insert(Projetos).values(Id=result+1, Name=parametros[0]['projeto'], \
                                          ClientesId=resultNw, \
                                          DataInicio=datetime.strptime(parametros[0]['dtinicio'], '%d/%m/%Y'), \
                                          DataFim=datetime.strptime(parametros[0]['dtfim'], '%d/%m/%Y'))

            try:
                self.session.execute(dml)
                self.session.commit()
            except:
                pass

        dql = 'select count(*) from Atividades'
        result = self.session.execute(dql)
        result = (list(result)[0])[0]

        if result == 0:
            dql = select(Projetos.Id).where(Projetos.Name == parametros[0]['projeto'])
            result = self.session.execute(dql)
            result = (list(result)[0])[0]

            dml = insert(Atividades).values(Id=1, Descricao=parametros[0]['descricao'], ProjetosId=result)

            self.session.execute(dml)
            self.session.commit()

        else:
            dql = 'select max(Id) from Atividades'
            result = self.session.execute(dql)
            result = (list(result)[0])[0]

            dql = select(Projetos.Id).where(Projetos.Name == parametros[0]['projeto'])
            resultNw = self.session.execute(dql)
            resultNw = (list(resultNw)[0])[0]

            dml = insert(Atividades).values(Id=result+1, Descricao=parametros[0]['descricao'], ProjetosId=resultNw)

            try:
                self.session.execute(dml)
                self.session.commit()
            except:
                pass

    def DqlExecute(self, stmt=None):

        result = self.session.execute(stmt)

        return result