import requests
import webbrowser
import sys
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.chrome.options import Options as COpt
from bs4 import BeautifulSoup

URL = sys.argv[1]
theDriver = './drivers/geckodriver'
option = FFOpt()
if sys.argv[2] != 'firefox.desktop':
    option=COpt()
    theDriver = './drivers/chromedriver'


option.headless = True
browser = webdriver.Firefox(options = option, executable_path = theDriver)
browser.get(URL)

with open('neoutput.html','wt',encoding = 'utf-8') as f:
    f.write(browser.page_source)

results = soup.find(id = 'ProductBuy')
themessage = results.find_all('button', class_ = 'btn btn-primary btn-wide')

if re.search("Add", themessage):
    webbrowser.open_new(URL)
