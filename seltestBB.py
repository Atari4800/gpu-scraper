from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
import requests, sys, webbrowser

URL='https://www.bestbuy.com/'

option = Options()
option.headless = True
browser=webdriver.Firefox(options=option, executable_path = './drivers/geckodriver')
browser.get(URL)
print(browser.page_source)
