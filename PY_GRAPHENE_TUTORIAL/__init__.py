# -*- encoding:utf-8 -*-


import os
import csv
import logging as log
from itertools import count


log.basicConfig(format='%(asctime)s|(levelName)s|%(funcName)s|%(lineno)d|%(message)s',
                filename='./RADIOS_TRUNKS_v1CEC.log', level=log.INFO)


class PATH:
    def __init__(self, root = '.'):
        self.sRoot = root

    def findFile(self):
        file = iter(os.listdir(self.sRoot))
        return file


class READ(PATH):
    def __init__(self, root = '.'):
        PATH.__init__(self, root)

    def reading(self):
        log.info('sasasa')
        with open(f'{self.sRoot}/{next(self.findFile())}', newline='') as f:
            read = iter(csv.reader(f, delimiter=';'))
            sequence = count(start=0, step=1)

            while True:
                print(next(sequence))
                try:
                    print(next(read))

                except StopIteration:
                    break


if __name__ == '__main__':
    r = READ('./FILES')
    r.reading()