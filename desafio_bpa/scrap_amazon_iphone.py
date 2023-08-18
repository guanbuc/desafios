#-*- encoding: utf-8 -*-
from urllib.request import urlopen
from bs4 import BeautifulSoup as BS
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.webdriver import Service
#from selenium.webdriver.common.keys import Keys
#from selenium.webdriver.common.by import By
import xlsxwriter as XLSX
import time


cap = DesiredCapabilities().FIREFOX
cap['marionette'] = False


class URLLIB:

    def __init__(self, sUrl = None):
        self._url = sUrl

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, new_url):
        self._url = new_url

    def openUrl(self, parUrl):
        try:
            url = urlopen(parUrl, timeout=6000)
            url_page = url.read()
            return url_page.decode('charmap')
        except:
            self.openUrl(parUrl)


class CRAWLER(URLLIB):

    def __init__(self, sUrl = None, sItem = None, sHTMLParser = None, *aTag):
        super().__init__(sUrl)
        self._item = sItem
        self._HTMLParser = sHTMLParser
        self.__tag = aTag
        self.workbook = XLSX.Workbook('./apple_iphone_products_and_price_founded.xlsx')
        self.worksheet = self.workbook.add_worksheet('apple_products')
        self.soup = ''

    @property
    def item(self):
        return self._item

    @item.setter
    def item(self, new_item):
        self._item = new_item

    @property
    def HTMLParser(self):
        return self._HTMLParser

    @HTMLParser.setter
    def HTMLParser(self, new_HTMLParser):
        self._HTMLParser = new_HTMLParser

    @property
    def tag(self):
        return self.__tag

    @tag.setter
    def tag(self, new_tag):
        self.__tag = new_tag

    def htmlDrag(self):
        self.worksheet.write(0,0,'product')
        self.worksheet.write(0,1,'price')

        def assemblerWkb(parTag):
            sText = ''
            iTake_parcels = 0
            iRows = 0

            try:
                self.soup = BS(parTag, 'html.parser', exclude_encodings=['iso-8859-7'])
                for s in self.soup.find_all(self.__tag[0],self.__tag[2]):
                    if self.__tag[2][0] in ' '.join(l for l in s.get(self.__tag[1])) and self._item.lower() in s.string.lower():
                        iTake_parcels = 1
                        sText = s.string
                    elif self.__tag[2][1] in ' '.join(l for l in s.get(self.__tag[1])) and iTake_parcels == 1:
                        iRows += 1
                        self.worksheet.write(iRows, iTake_parcels - 1, str(sText.replace(chr(10),'')).encode('ISO-8859-1').decode('utf8'))
                        iTake_parcels += 1
                        sText = s.string
                        self.worksheet.write(iRows, iTake_parcels - 1, str(sText.replace(chr(10),'')).encode('ISO-8859-1').decode('utf8'))

                    assemblerWkb(s)

            except Exception as a:
                pass

        assemblerWkb(self._HTMLParser)
        self.workbook.close()

class SCRAPING(CRAWLER):

    def __init__(self, sElementItem = None, sUrl = None, sItem = None, sHTMLParser = None, *aTag):
        super().__init__(sUrl, sItem, sHTMLParser, *aTag)
        self.drive = ''
        self.__elementItem = sElementItem

    @property
    def elementItem(self):
        return self.__elementItem

    @elementItem.setter
    def elementItem(self, new_elementItem):
        self.__elementItem = new_elementItem

    def searchItem(self):
        #self.drive = webdriver.Firefox(capabilities=cap, executable_path="C:\\Program Files (x86)\\Mozilla Firefox\\geckodriver.exe")
        #self.drive = webdriver.Chrome(executable_path='C:\\Program Files\\Google\\Chrome\\Application\\chromedriver.exe')
        self.drive = webdriver.Chrome(executable_path='/usr/bin/chromedriver')
        self.drive.get(self._url)
        input_product = self.drive.find_element_by_id(self.__elementItem)
        input_product.send_keys(str(self._item))
        input_product.submit()
        time.sleep(1)

        while self._HTMLParser == None:
            self._HTMLParser = self.openUrl(self.drive.current_url)

        self._HTMLParser

    def driveClose(self):
        self.drive.close()


if __name__ == '__main__':
    #binary = FirefoxBinary('C:\Program Files (x86)\Mozilla Firefox')
    clsSC = SCRAPING('twotabsearchtextbox', 'https://www.amazon.com.br', 'iphone')
    clsSC.searchItem()

    htmlP = clsSC._HTMLParser

    clsCR = SCRAPING('twotabsearchtextbox', 'https://www.amazon.com.br', 'iphone',
                     htmlP, 'span', 'class', ['a-size-base-plus a-color-base a-text-normal', 'a-offscreen'])

    clsCR.htmlDrag()
    clsSC.driveClose()