# -*- encoding: utf-8 -*-
import pandas as pd


class READ:

    def __init__(self, File=None, dlmt='|'):
        self.__File = File
        self.__dlmt = dlmt
        self.dtf = pd.DataFrame({})

    @property
    def File(self):
        return self.__File

    @File.setter
    def File(self, new_File):
        self.__File = new_File

    @property
    def dlmt(self):
        return self.__dlmt

    @dlmt.setter
    def dlmt(self, new_dlmt):
        self.__dlmt = new_dlmt

    def readFile(self):
        self.dtf = pd.read_csv(self.__File, sep=self.__dlmt, dtype='str', na_filter=False)

class ASSEMBLER_DTF(READ):
    def __init__(self, File=None, dlmt='|'):
        super().__init__(File, dlmt)
        self.__dtf = self.dtf
        self.nwDtf = pd.DataFrame({})

    @property
    def dtf(self):
        return self.__dtf

    @dtf.setter
    def dtf(self, new_Dtf):
        self.__dtf = new_Dtf

    def dateTanslate(self):
        try:
            self.__dtf['exhibition_date'] = pd.to_datetime(self.__dtf['exhibition_date'],
                                                           format='%Y-%m-%d', errors='coerce')
            self.__dtf['program_start_time'] = pd.to_datetime(self.__dtf['program_start_time'],
                                                              format='%Y-%m-%d %H:%M:%S', utc=False)
            self.__dtf['average_audience'] = self.__dtf['average_audience'].astype('float64')

        except KeyError:
            self.__dtf['date'] = pd.to_datetime(self.__dtf['date'],
                                                format='%d/%m/%Y', errors='coerce')
            self.__dtf['available_time'] = self.__dtf['available_time'].astype('int64')

        else:
            self.__dtf = self.__dtf

        finally:
            pass

    def addColDW(self):
        try:
            self.__dtf['weekday'] = self.__dtf['exhibition_date'].dt.dayofweek
            self.__dtf.drop(self.__dtf.columns[3], axis=1, inplace=True)

        except KeyError:
            self.__dtf['weekday'] = self.__dtf['date'].dt.dayofweek
            #self.__dtf['average_audience'] = 0
            #self.__dtf['average_audience'] = self.__dtf['average_audience'].astype('float64')
            #self.__dtf.drop(self.__dtf.columns[3], axis=1, inplace=True)

        else:
            self.__dtf = self.__dtf

        finally:
            pass

    def orderedCol(self):
        try:
            self.__dtf = self.__dtf.sort_values(by='exhibition_date', ascending=False)
            self.__dtf = self.__dtf.sort_values(by=['signal','program_code', 'weekday'])

        except KeyError:
            self.__dtf = self.__dtf.sort_values(by='date', ascending=True)
            self.__dtf = self.__dtf.sort_values(by=['signal','program_code', 'weekday'])

        else:
            self.__dtf = self.__dtf

        finally:
            pass

    def averagingGroupDf(self):
        self.readFile()
        self.dateTanslate()
        self.addColDW()
        self.orderedCol()

        self.__dtf = self.__dtf.groupby(['signal','program_code', 'weekday']).head(4)

        return self.__dtf.groupby(['signal', 'program_code', 'weekday']).mean()

        #self.__nwDtf.to_csv('./ouPutMean.csv')
        #self.__dtf = self.__dtf.groupby(['signal','program_code', 'weekday'])
        #self.__dtf = self.__dtf.filter(lambda x: len(x) < 6)
        #print(self.__dtf)

    def mergeDtf(self):
        self.readFile()
        self.dateTanslate()
        self.addColDW()
        self.orderedCol()

        self.nwDtf = pd.merge(self.__dtf, self.nwDtf, on=['signal','program_code', 'weekday'], how='left')
        #self.nwDtf.to_json( './ouPutMean.json', date_format='iso', date_unit='s', orient='columns')
        return self.nwDtf
        #return self.nwDtf.to_csv('./ouPutMean.csv', sep='|', index=False)