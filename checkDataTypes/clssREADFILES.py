# -*- encoding: utf-8 -*-


import pandas as pd
from clssFINDFILES import *


class READ(FILES):
    def __init__(self, File = None, dotExts = '.parquet'):
        super().__init__(dotExts)
        self._File = File

    @property
    def File(self):
        return self._FIle

    @File.setter
    def File(self, newFile):
        self._File = newFile

    def read_File(self):
        outPut = pd.read_parquet(self._File, engine = 'pyarrow')
        return outPut.read()