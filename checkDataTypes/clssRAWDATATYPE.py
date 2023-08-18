# -*- encoding: utf-8 -*-


import json as js
import pandas as pd
from clssREADFILES import *


class DATA(READ):
    def __init__(self, object = None, File = None, dotExts = None):
        super().__init__(File, dotExts)
        self._object = object
        self.json_description = {}
        self.json_Data_Type = {}
        self.json_Element_Item = {}

    @property
    def object(self):
        return self._object

    @object.setter
    def object(self, newObject):
        self._object = newObject

    def disser_DataType(self):
        nullSurveys = 0
        nullsWich = []
        self.json_description['data'] = []
        FileJ = open(f'{self.File.split(self._dotExts)[0]}_layout.json', 'w')

        for Data, Type in self._object.head().dtypes.items():
            self.json_Data_Type[Data] = []
            nullSurveys += 1 if self.crowled_DataType((Data, Type)) else 0
            nullsWich.append(Data) if self.crowled_DataType((Data, Type)) else None
            self.json_Data_Type[Data].append(self.json_Element_Item)

        self.json_description['data'].append(self.json_Data_Type)

        self.json_description['nulls'] = []
        self.json_Element_Item = {}
        self.json_Element_Item['nullSurveys'] = nullSurveys
        self.json_Element_Item['nullWichAre'] = nullsWich
        self.json_description['nulls'].append(self.json_Element_Item)

        FileJ.write('%s/n' % js.dumps(self.json_description, sort_keys=True, indent=4))
        FileJ.close()

        self._object.head().to_csv(f'{self._File.split(self._dotExts)[0]}_layout.csv', index=False)


    def crowled_DataType(self, parDataType):
        self.json_Element_Item = {}

        bNan = True if self._object.head().shape[0] == self.show_Nan(parDataType[0]) else False

        if 'object' in str(parDataType[1]):
            self.json_Element_Item['type'] = 'varchar2'

        elif 'int64' in str(parDataType[1]):
            self.json_Element_Item['type'] = 'integer'

        elif 'float64' in str(parDataType[1]):
            self.json_Element_Item['type'] = 'number'
            self.len_Dec_Float(parDataType[0])

        elif 'bool' in str(parDataType[1]):
            self.json_Element_Item['type'] = 'boolean'

        elif 'datetime64' in str(parDataType[1]):
            self.json_Element_Item['type'] = 'date'

        elif 'timedelta[ns]' in str(parDataType[1]):
            self.json_Element_Item['type'] = parDataType[1]

        elif 'category' == str(parDataType[1]):
            self.json_Element_Item['type'] = parDataType[1]

        self.json_Element_Item['nullAble'] = True if self.show_Nan(parDataType[0]) != 0 else False

        if bNan == False:
            self.sts_DataType(parDataType[0])

        return bNan

    def sts_DataType(self, parData):
        try:
            self.json_Element_Item['max'] = str(self._object.head()[parData].str.len().max())
            self.json_Element_Item['min'] = str(self._object.head()[parData].str.len().min())

        except AttributeError:
            self.json_Element_Item['max'] = str(self._object.head()[parData].values.max())
            self.json_Element_Item['min'] = str(self._object.head()[parData].values.min())

        except:
            self.json_Element_Item['max'] = str(self._object.head()[parData].values.max())
            self.json_Element_Item['min'] = str(self._object.head()[parData].values.min())
            self.json_Element_Item['avg'] = str(self._object.head()[parData].values.mean().round(2))

    def show_Nan(self, parData):
        cNan = 0

        try:
            for Value in self._object.head()[parData].values:
                if Value == '' or pd.isna(Value):
                    cNan += 1

            return cNan

        except:
            pass

    def len_Dec_Float(self, parData):
        nDec = 0

        for Value in self._object.head()[parData].values:
            if (len(str(Value)) - str(Value).find('.') - 1) >= nDec:
                nDec = len(str(Value)) - str(Value).find('.') - 1

        self.json_Element_Item['decNumber'] = nDec
