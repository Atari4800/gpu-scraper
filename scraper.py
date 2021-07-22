"""
This script runs a web scraper and searches for specific parameters within a webpage.
"""
# import os
# import requests
import sys
# import webbrowser
# import re
from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options as FFOpt
# from bs4 import BeautifulSoup

class Scraper:
    """
    This class handles web scraping operations.
    """

    def __init__(self, url, url_type):
        """
        Instantiates a web scraper and pulls initial page source information.
        :param url: The url of a link that will be scraped to find product information
        :param url_type: The type of link that a url is
                        BB - Bestbuy
                        NE - Newegg
                        BH - B&H
        """
        self.url = None
        self.soup = None
        self.store_label = None
        self.soup = None
        if url_type is not None and url is not None:
            self.the_driver = './drivers/geckodriver'
            self.option = FFOpt()
            self.option.headless = True
            try:
                self.browser = webdriver.Firefox(options=self.option, executable_path=self.the_driver)
            except Exception:
                print(
                    "Could not find the driver. Ensure that the \'geckodriver\' is in the directory: "
                    "./drivers/geckodriver")
                exit(-1)
            try:
                self.browser.get(url)
            except Exception:
                print("Could not obtain browser information. Are you sure that is a Newegg, Bestbuy, or B&H link?")
                exit(-1)

            self.strip_meta_characters(str(self.browser.page_source))
            self.browser.close()
            self.url = url
            self.store_label = url_type

    def strip_meta_characters(self, results):
        if results is not None:
            meta_char_list = [".","^","$","+","?","{","}","[","]","\\","|","(",")","\t","\n"]

            for i in meta_char_list:
                results = results.replace(i, " ")

            self.soup = results
        else:
            print("WARNING NONE RESULTS")
        return results

    def get_bb(self):
        """
        Searches for whether or not the HTML source grabbed by the scraper contains a product available for purchase
        with BestBuy :return: 0 if the product is not found available for purchase. :return: 1 if the product is
        found and available for purchase.
        """

        print(len(self.soup))

        if self.soup is None:
            return 0
        self.soup = self.soup[int(len(self.soup) * 0.25):]
        result = self.soup.find("Add to Cart")
        if result != -1:
            print("len(self.soup")
            print(result)
            return 1
        print(result)
        return 0

    def get_bh(self):
        """
        Searches for whether or not the HTML source grabbed by the scraper contains a product available for purchase
        with B&H :return: 0 if the product is not found available for purchase. :return: 1 if the product is found
        and available for purchase.
        """
        print(len(self.soup))
        if self.soup is None:
            return 0
        self.soup = self.soup[int(len(self.soup) * 0.25):]
        # print(len(self.soup))
        result = self.soup.find("Add to Cart")
        if result != -1 and self.soup:
            print("len(self.soup")
            # webbrowser.open_new(self.url)
            print(result)
            return 1
        print(result)
        print("Did B&H Bot detection find you? Open your browser and collect some cookies!!!")
        return 0

    def get_ne(self):
        """
        Searches for whether or not the HTML source grabbed by the scraper contains a product available for purchase
        with Newegg :return: 0 if the product is not found available for purchase. :return: 1 if the product is found
        and available for purchase.
        """
        print(len(self.soup))
        if self.soup is None:
            return 0
        self.soup = self.soup[int(len(self.soup) * 0.55):]
        print(len(self.soup))
        result = self.soup.find("Add to cart")
        if result != -1:
            print("It was found at", result)
            return 1

        return 0


if __name__ == '__main__':
    url = sys.argv[1]
    store_label = sys.argv[2]
    sc = scraper(url, store_label)
    if store_label == 'BB' or store_label == 'BH':
        exit(sc.get_bb())
    elif store_label == 'NE':
        exit(sc.get_ne())
    else:
        print("Invalid type")
        exit(0)
