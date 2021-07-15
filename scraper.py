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
            self.soup = BeautifulSoup(self.browser.page_source,'html.parser')
            self.browser.close()
            self.URL=URL
            self.uType=uType



    def getBB(self):
        """
        Searches for whether or not the HTML source grabbed by the scraper contains a product available for purchase with BestBuy
        :return: 0 if the product is not found available for purchase.
        :return: 1 if the product is found and available for purchase.
        """
        results = self.soup.find(class_ = 'fulfillment-add-to-cart-button')
        if results != None:
            if re.search("Add to Cart", str(results)):
                webbrowser.open_new(self.URL)
                return 1
        return 0

    def getBH(self):
        """
        Searches for whether or not the HTML source grabbed by the scraper contains a product available for purchase with B&H
        :return: 0 if the product is not found available for purchase.
        :return: 1 if the product is found and available for purchase.
        """
        results = self.soup.find(class_='cartRow_2dS2mdogHYAqhmKoANr6Ol')
        if results != None:
            if re.search("Add to Cart", str(results)):
                webbrowser.open_new(self.URL)
                return 1
        print(self.soup.prettify())
        print("Did B&H Bot detection find you? Open your browser and collect some cookies!!!")
        return 0

    def getNE(self):
        """
        Searches for whether or not the HTML source grabbed by the scraper contains a product available for purchase with Newegg
        :return: 0 if the product is not found available for purchase.
        :return: 1 if the product is found and available for purchase.
        """
        results = self.soup.find(class_='product-buy-box')
        if results == None:
            print("FML FUCKFACE")
            return 0
        if re.search("'>Add to cart <",str(results.find(id="ProductBuy"))):
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
