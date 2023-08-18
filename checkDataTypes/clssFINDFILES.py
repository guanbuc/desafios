# -*- encoding: utf-8 -*-


import os


class FILES:
    def __init__(self, dotExts = '.parquet'):
        self._dotExts = dotExts
        self.kFiles = {}
        self.kFiles[self._dotExts]=[]

    @property
    def dotExts(self):
        return self._dotExts

    @dotExts.setter
    def dotExts(self, newDotExts):
        self._dotExts = newDotExts

    def list_Dir(self, parDir = '.'):
        path = ''

        for i in os.listdir(parDir):
            path = '%s/%s' % (parDir, i)
            if os.path.isdir(path):
                if self.check_Permisioned(path):
                    self.list_Dir(path)

            self.is_File(path)


    def check_Permisioned(self, parPath):
        try:
            os.listdir(parPath)
            return True

        except Exception:
            return False

    def is_File(self, parFile):
        if os.path.isfile(parFile):
            if self._dotExts.lower() in parFile.lower():
                self.kFiles[self._dotExts].append(parFile)