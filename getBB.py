import requests
import sys
import webbrowser
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

soup = BeautifulSoup(browser.page_source, 'html.parser')
browser.close()
results = soup.find(class_ = 'fulfillment-add-to-cart-button')

if re.search("Add to Cart", str(results)):
    webbrowser.open_new(URL)


exit()
