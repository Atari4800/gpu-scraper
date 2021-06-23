import requests
import sys
import webbrowser
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options as FFOpt
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

with open('bboutput.html','wt', encoding = 'utf-8') as f:
    f.write(browser.page_source)

soup = BeautifulSoup(browser.page_source, 'html.parser')
results = soup.find(class_ = 'fulfillment-add-to-cart-button')

if re.search("Add to Cart", str(results)):
    webbrowser.open_new(URL)

browser.close()
