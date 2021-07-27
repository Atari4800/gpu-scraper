"""
This script runs a web scraper and searches for specific parameters within a webpage.
"""
# import os
# import requests
import sys
# import webbrowser
import re
from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options as FFOpt
from bs4 import BeautifulSoup



class Scraper:
    """
    This class handles web scraping operations.
    """

    def __get_source(url):
        """
        Retrieves a webpage's source code and creates a bs4 object from it

        :type url: string
        :param url: A valid URL

        :return: a bs4 object containing page source code.
        """
        the_driver = './drivers/geckodriver'
        option = FFOpt()
        option.headless = True
        try:
            browser = webdriver.Firefox(options=option, executable_path=the_driver)

        except Exception:
            print(
                "Could not find the driver. Ensure that the \'geckodriver\' is in the directory: "
                "./drivers/geckodriver")
            return -1

        # try:
        if not re.search("https", url) or not re.search("http", url):
            url = "https://" + url
        browser.get(url)
        """
        except Exception:
            print(
                "Could not find the driver. Ensure that the \'geckodriver\' is in the directory: "
                "./drivers/geckodriver")
            return -1
        """
        soup = BeautifulSoup(browser.page_source, features="lxml")
        browser.close()
        return soup
    @staticmethod
    def get_fields_bb(url, title, price):
        """
        Retrieves the name of a product, and a product's price from a bestbuy link.

        :type url: string
        :type url: the bestbuy url of a product

        :type title: string
        :param title: The name of a product to be added.

        :type price: double
        :param price: The price of a product to be added.
        """
        if not re.search("www.bestbuy.com/", url):
            return [None, None]
        page_source = Scraper.__get_source(url)
        if page_source is not None and not isinstance(page_source, int):
            if title is None:
                title = Scraper.__get_title_bb(page_source)
            if price is None:
                price = Scraper.__get_price_bb(page_source)
            return [title, price]
        return [None, None]
    @staticmethod
    def get_fields_ne(url, title, price):
        """
        Retrieves the name of a product, and a product's price from a newegg link.

        :type url: string
        :type url: the newegg url of a product

        :type title: string
        :param title: The name of a product to be added.

        :type price: double
        :param price: The price of a product to be added.
        """
        if not re.search("www.newegg.com/", url):
            return [None, None]
        page_source = Scraper.__get_source(url)
        if page_source is not None and not isinstance(page_source, int):
            if title is None:
                title = Scraper.__get_title_ne(page_source)
            if price is None:
                price = Scraper.__get_price_ne(page_source)
            return [title, price]
        return [None, None]
    @staticmethod
    def get_fields_bh(url, title, price):
        """
        Retrieves the name of a product, and a product's price from a b&h link.

        :type url: string
        :type url: the b&h url of a product

        :type title: string
        :param title: The name of a product to be added.

        :type price: double
        :param price: The price of a product to be added.
        """
        if not re.search("/www.bhphotovideo.com/", url):
            return [None, None]
        page_source = Scraper.__get_source(url)
        if page_source is not None and not isinstance(page_source, int):
            if title is None:
                title = Scraper.__get_title_bh(page_source)
            if price is None:
                price = Scraper.__get_price_bh(page_source)
            return [title, price]
        return [None, None]

    def __get_title_bh(soup):
        results = soup.find(class_='title_1S1JLm7P93Ohi6H_hq7wWh')
        if results is None:
            print("ERROR title not found. Cannot add product.")
            print(
                'B&H bot detection may have picked you up. Please increase product checking interval in the scheduler. Then go to B&H\'s website to do their recaptcha and try again.')
            return None
        title = results.get_text().split('BH')[0]
        return title

    def __get_price_bh(soup):
        results = soup.find(class_='price_1DPoToKrLP8uWvruGqgtaY')
        if results == None:
            print("ERROR price not found. Cannot add product.")
            return None
        price_str = results.get_text()
        price = float(price_str.split('$')[1].replace(',', ''))
        return price

    def __get_title_ne(soup):
        results = soup.find(class_='product-title')
        if results == None:
            print("ERROR title not found. Cannot add product.")
            return None
        title = str(results)[len('<h1 class=\"product-title\">'):-len('</h1>')]
        return title

    def __get_price_ne(soup):
        results = soup.find(class_='product-price')
        if results == None:
            print("ERROR price not found. Cannot add product.")
            return None
        price_str = results.get_text()
        if re.search('Sale', price_str):
            price = re.findall(r"\d+\.\d+", price_str)
            return float(price[0])
            # price = re.findall("d+.d+", price_str)
            if price == None:
                print("ERROR price not found. Cannot add product.")
                return None
            price = float(price[0])

        else:
            price = float(price_str.split('$')[1].replace(',', ''))
            return price

    def __get_title_bb(soup):
        results = soup.find(class_='sku-title')
        if results == None:
            print("ERROR title not found. Cannot add product.")
            return None
        results = results.find(class_='heading-5 v-fw-regular')
        if results == None:
            print("ERROR title not found. Cannot add product.")
            return None
        title = str(results)[len('h1 class = \"heading-5 v-fw-regular\"'):-len('</h1>')]
        return title

    def __get_price_bb(soup):
        results = soup.find(class_='priceView-hero-price priceView-customer-price')
        if results == None:
            print("ERROR price not found. Cannot add product.")
            return None
        price_str = str(results)
        price = float(price_str[price_str.index('aria-hidden="true">') + len('aria-hidden="true">') + 1:price_str.index(
            '</span><span class')].replace(',', ''))
        return price

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
        self.store_type = None
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
            self.store_type = url_type

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
    sc = Scraper(url, store_label)
    if store_label == 'BB' or store_label == 'BH':
        exit(sc.get_bb())
    elif store_label == 'NE':
        exit(sc.get_ne())
    else:
        print("Invalid type")
        exit(0)
