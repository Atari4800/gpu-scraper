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


class scraper:
    """
    This class handles web scraping operations.
    """

    def __init__(self, url, u_type):
        """
        Instantiates a web scraper and pulls initial page source information.
        :param url: The URL of a link that will be scraped to find product information
        :param u_type: The type of link that a URL is
                        BB - Bestbuy
                        NE - Newegg
                        BH - B&H
        """
        if u_type is not None:
            self.theDriver = './drivers/geckodriver'
            self.option = FFOpt()
            self.option.headless = True
            try:
                self.browser = webdriver.Firefox(options=self.option, executable_path=self.theDriver)
            except:
                print(
                    "Could not find the driver. Ensure that the \'geckodriver\' is in the directory: "
                    "./drivers/geckodriver")
                exit(-1)
            try:
                self.browser.get(url)
            except:
                print("Could not obtain browser information. Are you sure that is a Newegg, Bestbuy, or B&H link?")
                exit(-1)
            self.soup = BeautifulSoup(self.browser.page_source, 'html.parser')
            self.browser.close()

    def getbb(self):
        """
        Searches for whether or not the HTML source grabbed by the scraper contains a product available for purchase
        with BestBuy :return: 0 if the product is not found available for purchase. :return: 1 if the product is
        found and available for purchase.
        """
        results = self.soup.find(class_='fulfillment-add-to-cart-button')
        if results is not None:
            if re.search("Add to Cart", str(results)):
                webbrowser.open_new(URL)
                return 1
        return 0

    def getbh(self):
        """
        Searches for whether or not the HTML source grabbed by the scraper contains a product available for purchase
        with B&H :return: 0 if the product is not found available for purchase. :return: 1 if the product is found
        and available for purchase.
        """
        results = self.soup.find(class_='cartRow_2dS2mdogHYAqhmKoANr6Ol')
        if results is not None:
            if re.search("Add to Cart", str(results)):
                webbrowser.open_new(URL)
                return 1
        return 0

    def getne(self):
        """
        Searches for whether or not the HTML source grabbed by the scraper contains a product available for purchase
        with Newegg :return: 0 if the product is not found available for purchase. :return: 1 if the product is found
        and available for purchase.
        """
        results = self.soup.find(id='ProductBuy')
        if results is None:
            return 0
        themessage = results.find_all('button', class_='btn btn-primary btn-wide')
        if themessage is None:
            for themessage in themessage:
                if 'Add' in themessage.text:
                    webbrowser.open_new(URL)
                    return 1
        return 0


URL = sys.argv[1]
uType = sys.argv[2]
sc = scraper(URL, uType)
if __name__ == '__main__':
    if uType == 'BB':
        exit(sc.getbb())
    elif uType == 'NE':
        exit(sc.getne())
    elif uType == 'BH':
        exit(sc.getbh())
    else:
        print("Invalid type")
        exit(0)
