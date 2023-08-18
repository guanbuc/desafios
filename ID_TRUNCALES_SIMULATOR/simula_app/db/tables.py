# -*- encoding:utf-8 -*-


import datetime as dt
from sqlalchemy import *
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class CONVERSION_AIDS:
    def dataConvert(self, parDt):
        try:
            return dt.datetime.strftime(parDt, '%Y-%m-%d %H:%M:%S')

        except:
            return dt.datetime.strptime(parDt, '%Y-%m-%d %H:%M:%S')

class SEGMENT_ID_TESTE(Base):
    __tablename__ = 'SEGMENT_ID_TESTE'
    SI_ID = Column(Numeric, primery_key=True)
    SI_ID_TRONCAL = Column(Numeric)
    SI_EQUIP_A = Column(VARCHAR(50))
    SI_PORT_NAME_A = Column(VARCHAR(50))
    SI_TECNOLOGIA_A = Column(VARCHAR(20))
    SI_EQUIP_Z = Column(VARCHAR(50))
    SI_PORT_NAME_Z = Column(VARCHAR(50))
    SI_TECNOLOGIA_Z = Column(VARCHAR(20))
    SI_STATUS = Column(Numeric)
    SI_CREATE_DT = Column(Date)
    SI_USER = Column(VARCHAR(255))
    SI_DOCKUORDER = Column(Numeric)

class DB(CONVERSION_AIDS):
    SQL_ALCHEMY_DATABASE_URI = 'oracle+cx_oracle://sysdba:000000@192.168.56.105:1521/service_name=bratus&encoding=UTF-8&nencoding=UTF-8'
    Engine = create_engine(SQL_ALCHEMY_DATABASE_URI)
    Session = sessionmaker(bind=Engine, autocommit=False)

    def __init__(self):
        self.session = self.Session()
        self.Main = {}

    def ddlCreateTables(self):
        Base.metadata.create_all(self.Engine)

    def ddlStmt(self):
        self.ddlCreateTables()
        table1 = table('SEGMENT_ID', \
                       column('SI_ID'), \
                       column('SI_ID_TRONCAL'), \
                       column('SI_EQUIP_A'), \
                       column('SI_PORT_NAME_A'), \
                       column('SI_TECNOLOGIA_A'), \
                       column('SI_EQUIP_Z'), \
                       column('SI_PORT_NAME_Z'), \
                       column('SI_TECNOLOGIA_Z'), \
                       column('SI_STATUS'), \
                       column('SI_CREATE_DT'), \
                       column('SI_USER'), \
                       column('SI_DOKUORDER'))

        table2 = table('SEGMENT_ID_TESTE', \
                       column('SI_ID'), \
                       column('SI_ID_TRONCAL'), \
                       column('SI_EQUIP_A'), \
                       column('SI_PORT_NAME_A'), \
                       column('SI_TECNOLOGIA_A'), \
                       column('SI_EQUIP_Z'), \
                       column('SI_PORT_NAME_Z'), \
                       column('SI_TECNOLOGIA_Z'), \
                       column('SI_STATUS'), \
                       column('SI_CREATE_DT'), \
                       column('SI_USER'), \
                       column('SI_DOKUORDER'))

        stmt = table2.insert().from_select(['SI_ID', \
                                           'SI_ID_TRONCAL', \
                                           'SI_EQUIP_A', \
                                           'SI_PORT_NAME_A', \
                                           'SI_TECNOLOGIA_A', \
                                           'SI_EQUIP_Z', \
                                           'SI_PORT_NAME_Z', \
                                           'SI_TECNOLOGIA_Z', \
                                           'SI_STATUS', \
                                           'SI_CREATE_DT', \
                                           'SI_USER', \
                                           'SI_DOKUORDER'], table1.select())

        try:
            self.session.execute(stmt)
            self.session.commit()

        except:
            self.session.rollback()
            raise

        finally:
            self.session.close()

    def dqlStmt(self, pMain):
        self.Main = {}

        try:
            self.ddlStmt()

        except:
            pass

        if 'API_modif' in pMain.values():
            SI_ID_TRONCAL = pMain['SI_ID_TRONCAL']

            dql = "SELECT SI_ID, SI_ID_TRONCAL, " \
                  "SI_EQUIP_A, SI_PORT_NAME_A, SI_TECNOLOGIA_A, " \
                  "SI_EQUIP_Z, SI_PORT_NAME_Z, SI_TECNOLOGIA_Z, " \
                  "SI_STATUS, SI_DOKUORDER, SI_CREATE_DT, SI_USER FROM SEGMENT_ID_TESTE " \
                  f"WHERE SI_ID_TRONCAL LIKE '%{SI_ID_TRONCAL}%'" \
                  f" OR SI_EQUIP_A LIKE '%{SI_ID_TRONCAL}%'" \
                  f" OR SI_PORT_NAME_A LIKE '%{SI_ID_TRONCAL}%'" \
                  f" OR SI_TECNOLOGIA_A LIKE '%{SI_ID_TRONCAL}%'" \
                  f" OR SI_EQUIP_Z LIKE '%{SI_ID_TRONCAL}%'" \
                  f" OR SI_PORT_NAME_Z LIKE '%{SI_ID_TRONCAL}%'" \
                  f" OR SI_TECNOLOGIA_Z LIKE '%{SI_ID_TRONCAL}%'" \
                  " ORDER BY 1 DESC"

            resultA = self.session.execute(dql)

            for row in resultA:

                if row[2] is not None:
                    self.Main['SI_ID'] = row[0]
                    self.Main['SI_ID_TRONCAL'] = row[1]
                    self.Main['SI_EQUIP_A'] = row[2]
                    self.Main['SI_PORT_NAME_A'] = row[3]
                    self.Main['SI_TECNOLOGIA_A'] = row[4]
                    self.Main['SI_EQUIP_Z'] = row[5]
                    self.Main['SI_PORT_NAME_Z'] = row[6]
                    self.Main['SI_TECNOLOGIA_Z'] = row[7]
                    self.Main['SI_STATUS'] = row[8]
                    self.Main['SI_DOKUORDER'] = row[9]
                    self.Main['SI_CREATE_DT'] = self.dataConvert(row[10])
                    self.Main['SI_USER'] = row[11]

                    SI_EQUIP_A = row[2]
                    dql = f"SELECT LC_CLLI AS CLLI_A FROM LOCATION WHERE LC_NAME = trim('{SI_EQUIP_A}')"

                    resultB = self.session.execute(dql)

                    for row1 in resultB:
                        self.Main['CLLI_A'] = row1[0]

                    SI_EQUIP_Z = row[5]
                    dql = f"SELECT LC_CLLI AS CLLI_Z FROM LOCATION WHERE LC_NAME = trim('{SI_EQUIP_Z}')"

                    resultB = self.session.execute(dql)

                    for row1 in resultB:
                        self.Main['CLLI_Z'] = row1[0]

            return self.Main

        else:
            def case_0():
                SIID = f" AND SI_ID = '{pMain['SI_ID']}'" if pMain['SI_ID'] != '' else ''

                dql = "SELECT " \
                      " * " \
                      " FROM " \
                      " SEGMENT_ID_TESTE " \
                      " WHERE " \
                      f" TRIM(SI_EQUIP_A) = '{pMain['EQUIPO_A']}' " \
                      f" AND TRIM(SI_EQUIP_Z) = '{pMain['EQUIPO_Z']}'" \
                      f" AND TRIM(SI_PORT_NAME_A) = '{pMain['PORT_A']}'" \
                      f" AND TRIM(SI_PORT_NAME_Z)  = '{pMain['PORT_Z']}'" \
                      f" AND SI_STATUS IN (0, 1, 2)" \
                      f" {SIID}"

                result = self.session.execute(dql)

                for row in result:
                    datos = dict(zip(tuple(row.keys()), row))

                    if datos['SI_EQUIP_A'.lower()].strip() == pMain['EQUIPO_A'] and datos['SI_PORT_NAME_A'.lower()].strip() == pMain['PORT_A']:
                        return True

                    if datos['SI_EQUIP_Z'.lower()].strip() == pMain['EQUIPO_Z'] and datos['SI_PORT_NAME_Z'.lower()].strip() == pMain['PORT_Z']:
                        return True

                    if datos['SI_EQUIP_A'.lower()].strip() == pMain['EQUIPO_A'] and datos['SI_PORT_NAME_A'.lower()].strip() == pMain['PORT_A'] \
                        and datos['SI_EQUIP_Z'.lower()].strip() == pMain['EQUIPO_Z'] and datos['SI_PORT_NAME_Z'.lower()].strip() == pMain['PORT_Z']:
                        return True

            def case_1():
                SIID = f" AND SI_ID = '{pMain['SI_ID']}'" if pMain['SI_ID'] != '' else ''

                dql = "SELECT " \
                      " * " \
                      " FROM " \
                      " SEGMENT_ID_TESTE " \
                      " WHERE " \
                      f" TRIM(SI_EQUIP_A) = '{pMain['EQUIPO_A']}' " \
                      f" AND TRIM(SI_EQUIP_Z) = '{pMain['EQUIPO_Z']}'" \
                      f" AND TRIM(SI_PORT_NAME_A) = '{pMain['PORT_A']}'" \
                      f" AND TRIM(SI_PORT_NAME_Z)  = '{pMain['PORT_Z']}'" \
                      f" AND SI_STATUS IN (0, 1, 2)" \
                      f" {SIID}"

                result = self.session.execute(dql)

                for row in result:
                    datos = dict(zip(tuple(row.keys()), row))

                    if datos['SI_EQUIP_A'.lower()].strip() == pMain['EQUIPO_A'] and datos['SI_PORT_NAME_A'.lower()].strip() == pMain['PORT_A'] \
                        and datos['SI_EQUIP_Z'.lower()].strip() == pMain['EQUIPO_Z'] and datos['SI_PORT_NAME_Z'.lower()].strip() == pMain['PORT_Z']:
                        return True

            def case_2():
                SIID = f" AND SI_ID = '{pMain['SI_ID']}'" if pMain['SI_ID'] != '' else ''

                dql = "SELECT " \
                      " * " \
                      " FROM " \
                      " SEGMENT_ID_TESTE " \
                      " WHERE " \
                      f" ((TRIM(SI_EQUIP_A) = '{pMain['EQUIPO_A']}' " \
                      f" AND TRIM(SI_PORT_NAME_A) = '{pMain['PORT_A']}')" \
                      f" OR (TRIM(SI_EQUIP_Z) = '{pMain['EQUIPO_A']}'" \
                      f" AND TRIM(SI_PORT_NAME_Z)  = '{pMain['PORT_A']}'))" \
                      f" AND SI_STATUS IN (0, 1, 2)" \
                      f" {SIID}"

                result = self.session.execute(dql)

                for row in result:
                    datos = dict(zip(tuple(row.keys()), row))

                    if (datos['SI_EQUIP_A'.lower()].strip() == pMain['EQUIPO_A'] and datos['SI_PORT_NAME_A'.lower()].strip() == pMain['PORT_A']) \
                        or (datos['SI_EQUIP_A'.lower()].strip() == pMain['EQUIPO_A'] and datos['SI_PORT_NAME_A'.lower()].strip() == pMain['PORT_A']):
                        return True

            def case_3():
                SIID = f" AND SI_ID = '{pMain['SI_ID']}'" if pMain['SI_ID'] != '' else ''

                dql = "SELECT " \
                      " * " \
                      " FROM " \
                      " SEGMENT_ID_TESTE " \
                      " WHERE " \
                      f" ((TRIM(SI_EQUIP_A) = '{pMain['EQUIPO_Z']}' " \
                      f" AND TRIM(SI_PORT_NAME_A) = '{pMain['PORT_Z']}')" \
                      f" OR (TRIM(SI_EQUIP_Z) = '{pMain['EQUIPO_Z']}'" \
                      f" AND TRIM(SI_PORT_NAME_Z)  = '{pMain['PORT_Z']}'))" \
                      f" AND SI_STATUS IN (0, 1, 2)" \
                      f" {SIID}"

                result = self.session.execute(dql)

                for row in result:
                    datos = dict(zip(tuple(row.keys()), row))

                    if (datos['SI_EQUIP_Z'.lower()].strip() == pMain['EQUIPO_Z'] and datos['SI_PORT_NAME_Z'.lower()].strip() == pMain['PORT_Z']) \
                        or (datos['SI_EQUIP_Z'.lower()].strip() == pMain['EQUIPO_Z'] and datos['SI_PORT_NAME_Z'.lower()].strip() == pMain['PORT_Z']):
                        return True

            def case_4():
                x = 0

                SIID = f" AND SI_ID = '{pMain['SI_ID']}'" if pMain['SI_ID'] != '' else ''

                dql = "SELECT " \
                      " * " \
                      " FROM " \
                      " SEGMENT_ID_TESTE " \
                      " WHERE " \
                      f" TRIM(SI_EQUIP_A) = '{pMain['EQUIPO_A']}' " \
                      f" AND TRIM(SI_EQUIP_Z) = '{pMain['EQUIPO_Z']}'" \
                      f" AND SI_STATUS IN (0, 1, 2)" \
                      f" {SIID}"

                result = self.session.execute(dql)

                for row in result:
                    datos = dict(zip(tuple(row.keys()), row))
                    x+=1

                    if datos['SI_EQUIP_A'.lower()].strip() == pMain['EQUIPO_A'] and datos['SI_EQUIP_Z'.lower()].strip() == pMain['EQUIPO_Z']:
                        return True

            if pMain['SI_ID'] != '':
                if case_4():
                    return True

                else:
                    return False

            else:
                if True in{'0': case_0(),
                           '1': case_1(),
                           '2': case_2(),
                           '3': case_3()}:
                    return True

                else:
                    return False

    def dmlStmt(self, pMain):
        try:
            self.ddlStmt()

        except:
            pass

        sql = "SELECT " \
              " SI_ID_TRUNCAL " \
              " FROM " \
              " ( " \
              " SELECT " \
              " CASE " \
              " WHEN LENGTH(SUBSTR(max(SI_ID_TRONCAL), " \
              " REGEXP_INSTR(SUBSTR(max(SI_ID_TRONCAL), " \
              " 2, " \
              " LENGTH(MAX(SI_ID_TRONCAL))), " \
              " '[^0]', " \
              " 1) + 1, " \
              " LENGTH(MAX(SI_ID_TRONCAL))) + 1) < 9 THEN '3' || LPAD(TO_NUMBER(SUBSTR(MAX(SI_ID_TRONCAL), " \
              " REGEXP_INSTR(SUBSTR(MAX(SI_ID_TRONCAL), " \
              " 2, " \
              " LENGTH(MAX(SI_ID_TRONCAL))), " \
              " '[^0]', " \
              " 1) + 1, " \
              " LENGTH(MAX(SI_ID_TRONCAL)))) + 1, " \
              " 8, " \
              " 0) " \
              " ELSE '3' || TO_NUMBER(LPAD(1, " \
              " 8, " \
              " 0)) " \
              " END AS SI_ID_TRONCAL " \
              " FROM SEGMENT_ID_TESTE) "

        result = self.session.execute(sql)

        for row in result:
            IDGENERADO = row[0]

        if 'API_baja' in pMain.values():
            stmt = "UPDATE " \
                   " SEGMNET_ID_TESTE " \
                   " SET " \
                   "SI_STATUS = 4 " \
                   " WHERE " \
                   f"SI_ID = {pMain['SI_ID']}" \
                   " AND " \
                   f" SI_ID_TRONCAL = {pMain['SI_ID_TRONCAL']}"

            self.session.execute(stmt)
            self.session.commit()

            pMain['TYPE'] = 'DISCONNECTED'

            return pMain

        elif pMain['TYPE'] == 'API_alta':
            stmt = f"INSERT INTO SEGMENT_ID_TESTE " \
                   " (SI_ID_TRONCAL, SI_EQUIP_A, SI_PORT_NAME_A, SI_TECNOLOGIA_A, SI_EQUIP_Z, SI_PORT_Z, SI_TECNOLOGIA_Z, SI_STATUS, SI_CREATE_DT, SI_USER, SI_DOKUORDER) " \
                   f" VALUES ( '{IDGENERADO}'," \
                   f" '{pMain['EQUIPO_A']}', " \
                   f" '{pMain['PORTA_A']}', " \
                   f" '{pMain['TECNO_A']}', " \
                   f" '{pMain['EQUIPO_Z']}', " \
                   f" '{pMain['PORTA_Z']}', " \
                   f" '{pMain['TECNO_Z']}', " \
                   " 0, " \
                   f" TO_DATE('{self.dataConvert(dt.datetime.now())}', 'RRRR-MM-DD HH24:MI:SS'), " \
                   " 'AC89603', " \
                   " Null)"

            self.session.execute(stmt)
            self.session.commit()

            pMain['TYPE'] = 'REQUESTED'

            return pMain

        elif pMain['TYPE'] == 'API_modif':
            stmt = "UPDATE " \
                   " SEGMENT_ID_TESTE " \
                   " SET " \
                   f" SI_EQUIP_A = '{'EQUIPO_A'}', " \
                   f" SI_PORT_NAME_A = '{'PORTA_A'}', " \
                   f" SI_TECNOLOGIA_A = '{'TECNO_A'}', "\
                   f" SI_EQUIP_Z = '{'EQUIPO_Z'}', " \
                   f" SI_PORT_NAME_Z = '{'PORTA_Z'}', " \
                   f" SI_TECNOLOGIA_Z = '{'TECNO_Z'}', " \
                   " SI_USER = 'AC89603' " \
                   " WHERE " \
                   f" SI_ID = '{pMain['SI_ID']}'"

            self.session.execute(stmt)
            self.session.commit()

            pMain['TYPE'] = 'REQUESTED'

            return pMain