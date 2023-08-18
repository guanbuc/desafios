# -*- encoding: utf-8 -*-


import requests as req
import datetime as dt
import time
import json as js
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker, joinedload
from sqlalchemy.ext.declarative import declarative_base
from flask.views import MethodView
from flask import *
from app import app


Base = declarative_base()
KEYS = '1b32424caf1834c9810e8c96607fd300'
returnError = {'code':'404', 'message':'no data found!'}

class CONVERSION_AIDS:
    def dateConvert(self, parDt):
        #print(time.mktime((dt.date.today() - dt.timedelta(days=4)).timetuple()))
        try:
            return dt.datetime.strftime(dt.datetime.fromtimestamp(parDt), '%Y-%m-%d')
        except TypeError:

            try:
                return dt.datetime.strftime(parDt, '%Y-%m-%d')

            except:
                return dt.datetime.strptime(parDt, '%Y-%m-%d')

    def measurementConversion(self, parTemp):
        return self.roundD(parTemp - 273)

    def roundD(self, parDec):
        return '%.2f' % parDec


class WHEATER(Base):
    __tablename__ = 'WHEATER'
    id  = Column(Integer)
    temp = Column(Float)
    feels_like = Column( Float)
    temp_min = Column(Float)
    temp_max = Column(Float)
    pressure = Column(Integer)
    sea_level = Column(Integer)
    grnd_level = Column(Integer)
    humidity = Column(Integer)
    temp_kf = Column(Float)
    main = Column(VARCHAR)
    description = Column(VARCHAR)
    speed = Column(Float)
    gust = Column(Float)
    visibility = Column(Integer)
    dt = Column(DateTime)
    dt_txt = Column(DateTime, primary_key = True)
    idfk = Column(Integer, primary_key = True)


class CITY(Base):
    __tablename__ = 'CITY'
    idfk = Column(Integer, primary_key = True)
    name = Column(VARCHAR)
    lat = Column(Float)
    lon = Column(Float)
    country = Column(VARCHAR)
    population = Column(Integer)
    timezone = Column(Integer)
    sunrise = Column(Integer)
    sunset = Column(Integer)


class BD(CONVERSION_AIDS):
    def __init__(self):
        super(CONVERSION_AIDS, self).__init__()
        self.session = object

    def connectDB(self):
        db_string = 'postgresql://postgres:000000@192.168.56.103:5432/postgres'
        engine = create_engine(db_string)
        Session = sessionmaker(bind = engine)
        self.session = Session()
        return engine

    def ddlCreateTables(self):
        Base.metadata.create_all(self.connectDB())

    def dmlAssembler(self, **pInstruction):
        self.ddlCreateTables()
        if pInstruction.get('instruction') == 'i':
            if pInstruction.get('items') == 'city':
                add_CITY = CITY(idfk = pInstruction.get('data')[0]['idfk'],
                                name = pInstruction.get('data')[0]['name'],
                                lat = pInstruction.get('data')[0]['lat'],
                                lon = pInstruction.get('data')[0]['lon'],
                                country = pInstruction.get('data')[0]['country'],
                                population = pInstruction.get('data')[0]['population'],
                                timezone = pInstruction.get('data')[0]['timezone'],
                                sunrise = pInstruction.get('data')[0]['sunrise'],
                                sunset = pInstruction.get('data')[0]['sunset'])

                try:
                    self.session.add(add_CITY)
                    self.session.commit()

                except:
                    pass

            elif pInstruction.get('items') == 'wheater':
                for i in pInstruction.get('data')[0]:
                    try:
                        for l in self.session.query(func.max(WHEATER.id)):
                            for Value in l:
                                iPK = Value + i

                    except:
                        iPK = i

                    pInstruction.get('data')[0][i].update({'id':iPK})

                #print(pInstruction.get('data')[0])
                for i in pInstruction.get('data')[0]:
                    add_WHEATER = WHEATER(id=pInstruction.get('data')[0][i]['id'],
                                          temp=pInstruction.get('data')[0][i]['temp'],
                                          feels_like=pInstruction.get('data')[0][i]['feels_like'],
                                          temp_min=pInstruction.get('data')[0][i]['temp_min'],
                                          temp_max=pInstruction.get('data')[0][i]['temp_max'],
                                          pressure=pInstruction.get('data')[0][i]['pressure'],
                                          sea_level=pInstruction.get('data')[0][i]['sea_level'],
                                          grnd_level=pInstruction.get('data')[0][i]['grnd_level'],
                                          humidity=pInstruction.get('data')[0][i]['humidity'],
                                          temp_kf=pInstruction.get('data')[0][i]['temp_kf'],
                                          main=pInstruction.get('data')[0][i]['main'],
                                          description=pInstruction.get('data')[0][i]['description'],
                                          speed=pInstruction.get('data')[0][i]['speed'],
                                          gust=pInstruction.get('data')[0][i]['gust'],
                                          visibility=pInstruction.get('data')[0][i]['visibility'],
                                          dt=pInstruction.get('data')[0][i]['dt'],
                                          dt_txt=pInstruction.get('data')[0][i]['dt_txt'],
                                          idfk=pInstruction.get('data')[0][i]['idfk'])
                    try:
                        self.session.add(add_WHEATER)
                        self.session.commit()

                    except:
                        pass
                    #self.connectDB().execute(self.ddlWeather.insert(pInstruction.get('data')[0][i]))

    def dqlAssembler(self, **pInstruction):
        self.ddlCreateTables()
        if pInstruction.get('items') == 'city':
            result = self.session.query(func.count(WHEATER.dt).label('cont')).filter(WHEATER.idfk == CITY.idfk, CITY.name.like(pInstruction.get('name').title()), WHEATER.dt >= pInstruction.get('date')).group_by(CITY.name)

            try:
                return int(''.join(i.cont for i in result).replace('','0'))

            except:
                for i in result:
                    return i.cont

        elif pInstruction.get('items') == 'wheater':

            dataMain = {}
            dataMain['main'] = []
            dataMainItem = {}

            date = pInstruction.get('date') if pInstruction.get('date') != None else '1900-01-01'

            result = self.session.query(WHEATER.dt, CITY.name,
                                        func.avg(WHEATER.temp).label('temp'),
                                        func.avg(WHEATER.feels_like).label('feels_like'),
                                        func.avg(WHEATER.temp_min).label('temp_min'),
                                        func.avg(WHEATER.temp_max).label('temp_max'),
                                        func.avg(WHEATER.pressure).label('pressure'),
                                        func.avg(WHEATER.sea_level).label('sea_level'),
                                        func.avg(WHEATER.grnd_level).label('grnd_level'),
                                        func.avg(WHEATER.humidity).label('humidity'),
                                        func.avg(WHEATER.speed).label('speed'),
                                        func.avg(WHEATER.visibility).label('visibility')).filter(WHEATER.idfk == CITY.idfk, CITY.name.like(pInstruction.get('name').title()), WHEATER.dt >= date).group_by(WHEATER.dt, CITY.name).order_by(WHEATER.dt).all()

            for i in result:
                dataMainItem = {}
                if date == '1900-01-01':
                    dataMainItem['dt'] = self.dateConvert(i.dt)
                    dataMainItem['name'] = i.name
                    dataMainItem['temp'] = self.measurementConversion(i.temp)

                else:
                    dataMainItem['dt'] = self.dateConvert(i.dt)
                    dataMainItem['name'] = i.name
                    dataMainItem['temp'] = self.measurementConversion(i.temp)
                    dataMainItem['feels_like'] = self.measurementConversion(i.feels_like)
                    dataMainItem['temp_min'] = self.measurementConversion(i.temp_min)
                    dataMainItem['temp_max'] = self.measurementConversion(i.temp_max)
                    dataMainItem['pressure'] = self.roundD(i.pressure)
                    dataMainItem['sea_level'] = self.roundD(i.sea_level)
                    dataMainItem['grnd_level°'] = self.roundD(i.grnd_level)
                    dataMainItem['humidity'] = self.roundD(i.humidity)
                    dataMainItem['speed'] = self.roundD(i.speed)
                    dataMainItem['visibility'] = self.roundD(i.visibility)

                dataMain['main'].append(dataMainItem)

            return dataMain


class REQUEST_API(CONVERSION_AIDS):
    def __init__(self, url = 'http://'):
        super(CONVERSION_AIDS, self).__init__()
        self.sUrl = url
        self.content = ''
        self.index = ''
        self.iD = 0
        self.dataMain = {}
        self.dataSetItems = {}
        self.dataSetItemElement = {}

    def checkUrl(self):
        return True if req.get(self.sUrl).status_code == 200 else False

    def getData(self):
        if self.checkUrl():
            self.content = req.get(self.sUrl).json()
            self.jsonMount()

    def jsonMount(self):
        idfk = {}
        for i in self.content:
            def recGetData(content):
                if type(content) not in [list, dict]:
                    try:
                        if self.iD > -1:
                            if self.index not in ['pop', 'all', 'pod', 'deg', 'icon', '3h']:
                                if self.index == 'dt':
                                    self.dataSetItemElement[self.index] = self.dateConvert(content)

                                else:
                                    self.dataSetItemElement[self.index] = content

                        else:
                            self.dataSetItemElement[self.index if self.index != 'id' else 'idfk'] = content if self.index != 'name' else content.title()
                            if self.index == 'id':
                                idfk['idfk'] = content

                        if self.index == 'dt_txt':
                            self.iD += 1
                            self.dataSetItems[self.iD] = self.dataSetItemElement
                            self.dataSetItemElement = {}

                    except:
                        pass

                    return content

                elif type(content) == dict:
                    for ii in content:
                        self.index = ii

                        recGetData(content[self.index])

                else:
                    for ii in content:
                        recGetData(ii)


            self.index = i

            if self.index == 'city':
                self.iD = -1
                recGetData(self.content[self.index])
                for dsi in self.dataSetItems:
                    self.dataSetItems[dsi].update(idfk)

                self.dataMain['city'] = []
                self.dataMain['city'].append(self.dataSetItemElement)

            elif self.index == 'list':
                self.iD = 0
                recGetData(self.content[self.index])

                self.dataMain['wheater'] = []
                self.dataMain['wheater'].append(self.dataSetItems)


class API_ACTION(REQUEST_API):
    clBD = BD()
    def __init__(self, Main, url = 'http://'):
        super().__init__(url)
        self.__main = Main

    def requestRun(self):
        if self.clBD.dqlAssembler(items='city', name=self.__main['cidade'], date=self.dateConvert(dt.date.today())) < 5:
            self.sUrl = f'http://api.openweathermap.org/data/2.5/forecast?q={self.__main["cidade"]}&appid={KEYS}&lang=pt'
            self.getData()
            return self.dbRun()

        else:
            try:
                dql = self.clBD.dqlAssembler(items='wheater', name=self.__main['cidade'], date=self.__main['data'])

            except:
                dql = self.clBD.dqlAssembler(items='wheater', name=self.__main['cidade'])

            return make_response(jsonify(dql), 200)


    def dbRun(self):
        if len(self.dataMain) == 0:
            return make_response(jsonify(returnError), 400)

        else:
            for i in self.dataMain:
                self.clBD.dmlAssembler(instruction='i', items=i, data=self.dataMain[i])

            try:
                dql = self.clBD.dqlAssembler(items='wheater', name=self.__main['cidade'], date=self.__main['data'])

            except:
                dql = self.clBD.dqlAssembler(items='wheater', name=self.__main['cidade'])

            if len(dql['main']) == 0:
                return make_response(jsonify(returnError), 400)

            else:
                return make_response(jsonify(dql), 200)


class RESPONSE_API(MethodView):
    def get(self, **kMain):
        clAPI = API_ACTION(kMain)
        return clAPI.requestRun()


class WHEATER_API:
    def __init__(self, endpoint='RESPONSE'):
        self.__endpoint = endpoint

    def APIrun(self):
        url = '/wheaterguest/API/defaults/'
        pType = 'string'
        API = RESPONSE_API.as_view((self.__endpoint))

        app.add_url_rule(url, defaults={'cidade': None, 'data': None}, view_func=API, methods=['GET',])

        app.add_url_rule(url, view_func=API, methods=['GET',])

        app.add_url_rule(f'{url}cidade=<{pType}:cidade>', view_func=API, methods=['GET',])

        app.add_url_rule(f'{url}cidade=<{pType}:cidade>&data=<{pType}:data>', view_func=API, methods=['GET',])


if __name__ == '__main__':
    WHEATER_API().APIrun()
    app.run(debug=True)



