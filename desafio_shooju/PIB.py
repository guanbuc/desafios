# -*- encoding: utf-8 -*-


import zipfile as zip
import csv
import json
import os
from  urllib.request import *


class DOWNLOAD:


    def __init__(self, sUrl):
        super().__init__()
        self.url = sUrl

    def openUrl(self):
        try:
            self.url = urlretrieve(self.url, timeout=6000)
            self.url.read()

        except Exception:
            self.openUrl()


if __name__ == '__main__':
    clsDOWN = DOWNLOAD('https://www.jodidata.org/_resources/files/downloads/gas-data/jodi_gas_csv_beta.zip')
    clsDOWN.openUrl()
