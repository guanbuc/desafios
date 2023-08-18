#-*- encoding: utf-8 -*-

import zipfile
from datetime import datetime
import csv
import json
import os
from urllib.request import *


class PATH:

    def __init__(self, sPath = '.', sExtFile = '.zip'):
        self.__Path = sPath
        self.__ExtFile = sExtFile
        self.nameFile = []

    @property
    def sPath(self):
        return self.__Path

    @sPath.setter
    def sPath(self, newPath):
        self.__Path = newPath

    @property
    def sExtFile(self):
        return self.__ExtFile

    @sExtFile.setter
    def sExtFile(self, newExtFile):
        self.__ExtFile = newExtFile

    def listDir(self):
        for root in os.listdir(self.__Path):
            if root.endswith(self.__ExtFile):
                self.nameFile.append(root)

        return self.nameFile


class DOWNLOAD(PATH):

    def __init__(self, sUrl = None, sPath = '.', sExtFile = '.zip'):
        super().__init__(sPath, sExtFile)
        self.__Url = sUrl

    @property
    def sUrl(self):
        return self.__Url

    @sUrl.setter
    def sUrl(self, newUrl):
        self.__Url = newUrl

    def dwnUrl(self, parUrl = None):
        try:
            url = urlretrieve((self.__Url if parUrl == None else parUrl),
                                  (self.__Url if parUrl == None else parUrl).split('/')[len((self.__Url if parUrl == None else parUrl).split('/'))-1])
        except:
            print('404 - no data found')


class READ(PATH):

    def __init__(self, sPath = '.', sExtFile = '.zip'):
        super().__init__(sPath, sExtFile)
        self.Path = ''

    def extract(self, parZip):
        with zipfile.ZipFile(parZip, 'r') as zip:
            zip.extractall(f'./{parZip.split(chr(46))[0]}/')

        self.Path = f'./{parZip.split(chr(46))[0]}'

    def readCSV(self):
        clsP = PATH(self.Path, '.csv')

        for fileName in clsP.listDir():
            rCSV = open(f'{self.Path}/{fileName}', 'r')
            reader = csv.DictReader(rCSV)
            return reader


class ASSEMBLERJS(READ):

    def __init__(self):
        super().__init__()
        self.feed = {}
        self.feed['feed'] = []
        self.feedField = {}
        self.feedItem = {}
        self.feedPoint = []
        self.id = 0

    def datetimeFORMAT(self, parDateTime):
        return str(datetime.date(datetime.strptime(parDateTime, '%Y-%m')))

    def queryFields(self):
        with open('./jsonFile.json', 'w') as wJSON:
            wJSON.write(f'{chr(123)}"feed":[')

        for row in self.readCSV():
            self.feedItem = {}
            self.feedItem['REF_AREA'] = row['REF_AREA']
            self.feedItem['ENERGY_PRODUCT'] = row['ENERGY_PRODUCT']
            self.feedItem['FLOW_BREAKDOWN'] = row['FLOW_BREAKDOWN']
            self.feedItem['UNIT_MEASURE'] = row['UNIT_MEASURE']
            self.feedItem['ASSESSMENT_CODE'] = row['ASSESSMENT_CODE']

            self.feedPoint = []
            self.Fields(self.feedItem)

        with open('./jsonFile.json', 'a') as wJSON:
            wJSON.write(f'{chr(123)}{chr(125)}]{chr(125)}')

        #with open('./jsonFile.json', 'w') as wJSON:
            #wJSON.write(json.dumps(self.feed, indent=4))

    def queryPoints(self):
        for row in self.readCSV():
            if list(self.feedItem.values()) == [row['REF_AREA'], row['ENERGY_PRODUCT'], row['FLOW_BREAKDOWN'],
                                                row['UNIT_MEASURE'], row['ASSESSMENT_CODE']]:
                Points = [self.datetimeFORMAT(row['TIME_PERIOD']), row['OBS_VALUE']]
                self.feedPoint.append(Points)

    def Fields(self, parArgs):
        b = False
        for Values in self.feed.values():
            for i in Values:
                try:
                    if parArgs == i['campos']:
                        b = True

                except:
                    b = False

        if b == False:
            self.feedField = {}
            self.queryPoints()
            self.id +=1
            self.feedField['series_id'] = self.id
            self.feedField['points'] = self.feedPoint
            self.feedField['campos'] = parArgs
            with open('./jsonFile.json', 'a') as wJSON:
                wJSON.write(f'{json.dumps(self.feedField, indent=4)},\n')
            self.feed['feed'].append(self.feedField)


if __name__ == '__main__':
    clsD = DOWNLOAD('https://www.jodidata.org/_resources/files/downloads/gas-data/jodi_gas_csv_beta.zip')
    clsD.dwnUrl()
    clsD = DOWNLOAD('.', '.zip')
    clsR = READ()
    clsR.extract(clsR.listDir()[0])
    clsAJS= ASSEMBLERJS()
    clsAJS.Path = clsR.Path
    clsAJS.queryFields()