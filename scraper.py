"""
This script runs a web scraper and searches for specific parameters within a webpage.
"""
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
    """
    This class handles web scraping operations.
    """
    def __init__(self, URL, uType):
        """
        Instantiates a web scraper and pulls initial page source information.
        :param URL: The URL of a link that will be scraped to find product information
        :param uType: The type of link that a URL is
                        BB - Bestbuy
                        NE - Newegg
                        BH - B&H
        """
        self.URL = None
        self.soup = None
        self.uType = None
        self.soup = None
        if uType is not None and URL is not None:
            self.theDriver = './drivers/geckodriver'
            self.option = FFOpt()
            self.option.headless = True
            try:
                self.browser = webdriver.Firefox(options=self.option, executable_path=self.theDriver)
            except:
                print("Could not find the driver. Ensure that the \'geckodriver\' is in the directory: ./drivers/geckodriver")
                exit(-1)
            try:
                self.browser.get(URL)
            except:
                print("Could not obtain browser information. Are you sure that is a Newegg, Bestbuy, or B&H link?")
                exit(-1)
            self.soup = self.stripMetaCharacters(str(self.browser.page_source))
            self.browser.close()
            self.URL=URL
            self.uType=uType
    def stripMetaCharacters(self,results):

        results = results.replace("\."," ")
        results = results.replace("\^"," ")
        results = results.replace("\$", " ")
        results = results.replace("\+", " ")
        results = results.replace("\?", " ")
        results = results.replace("\{", " ")
        results = results.replace("\}", " ")
        results = results.replace("\[", " ")
        results = results.replace("\]", " ")
        results = results.replace("\\", " ")
        results = results.replace("\|", " ")
        results = results.replace("\(", " ")
        results = results.replace("\)", " ")
        results = results.replace("\t"," ")
        results = results.replace("\n", " ")
        self.soup = results
        return results



    def getBB(self):
        """
        Searches for whether or not the HTML source grabbed by the scraper contains a product available for purchase with BestBuy
        :return: 0 if the product is not found available for purchase.
        :return: 1 if the product is found and available for purchase.
        """


        if re.search("Add to Cart", str(self.soup)):
            print("It worked bitch.")
            webbrowser.open_new(self.URL)
            return 1
        return 0

    def getBH(self):
        """
        Searches for whether or not the HTML source grabbed by the scraper contains a product available for purchase with B&H
        :return: 0 if the product is not found available for purchase.
        :return: 1 if the product is found and available for purchase.
        """
        if re.search("Add to Cart", self.soup):
            webbrowser.open_new(self.URL)
            return 1

        print("Did B&H Bot detection find you? Open your browser and collect some cookies!!!")
        return 0

    def getNE(self):
        """
        Searches for whether or not the HTML source grabbed by the scraper contains a product available for purchase with Newegg
        :return: 0 if the product is not found available for purchase.
        :return: 1 if the product is found and available for purchase.
        """
        if re.search("Add to cart",self.soup):
            webbrowser.open_new(self.URL)
            return 1

        return 0


if __name__ == '__main__':
    URL = sys.argv[1]
    uType = sys.argv[2]
    sc = scraper(URL, uType)
    if uType == 'BB':
        exit( sc.getBB())
    elif uType == 'NE':
        exit(sc.getNE())
    elif uType == 'BH':
        exit(sc.getBH())
    else:
        print("Invalid type")
        exit(0)
