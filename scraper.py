import os

import requests
import sys
import webbrowser
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options as FFOpt
from bs4 import BeautifulSoup

class scraper :
    def __init__(self, URL, uType):
        if uType != None:
            self.theDriver = './drivers/geckodriver'
            self.option = FFOpt()
            self.option.headless = True
            self.browser = webdriver.Firefox(options=self.option, executable_path=self.theDriver)
            self.browser.get(URL)
            self.soup = BeautifulSoup(self.browser.page_source,'html.parser')
            self.browser.close()



    def getBB(self):
        results = self.soup.find(class_ = 'fulfillment-add-to-cart-button')
        if re.search("Add to Cart", str(results)):
            webbrowser.open_new(URL)
            return 1
        return 0

    def getBH(self):
        results = self.soup.find(class_='cartRow_2dS2mdogHYAqhmKoANr6Ol')
        if re.search("Add to Cart", str(results)):
            webbrowser.open_new(URL)
            return 1
        return 0

    def getNE(self):
        results = self.soup.find(id='ProductBuy')
        themessage = results.find_all('button', class_='btn btn-primary btn-wide')
        for themessage in themessage:
            if 'Add' in themessage.text:
                webbrowser.open_new(URL)
                return 1
        return 0

URL = sys.argv[1]
uType = sys.argv[2]
sc = scraper(URL, uType)
if uType == 'BB':
    exit( sc.getBB())
elif uType == 'NE':
    exit(sc.getNE())
else:
    exit(sc.getBH())
