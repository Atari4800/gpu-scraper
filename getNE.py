import requests
import webbrowser
import sys
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options as FFOpt
from bs4 import BeautifulSoup

URL = sys.argv[1]
theDriver = './drivers/geckodriver'
option = FFOpt()




option.headless = True
browser = webdriver.Firefox(options = option, executable_path = theDriver)

browser.get(URL)

soup = BeautifulSoup(browser.page_source,'html.parser')
browser.close()
results = soup.find(id = 'ProductBuy')
themessage = results.find_all('button', class_ = 'btn btn-primary btn-wide')
for themessage in themessage:
    if 'Add' in themessage.text:
        webbrowser.open_new(URL)


exit()
