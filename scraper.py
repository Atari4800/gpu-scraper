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

    @staticmethod
    def __get_source(my_url):
        """
        Retrieves a webpage's source code and creates a bs4 object from it

        :type my_url: string
        :param my_url: A valid URL

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
        if not re.search("https", my_url) or not re.search("http", my_url):
            my_url = "https://" + my_url
        browser.get(my_url)
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
    def get_fields_bb(my_url, title, price):
        """
        Retrieves the name of a product, and a product's price from a bestbuy link.

        :type my_url: string
        :param my_url: the bestbuy url of a product

        :type title: string
        :param title: The name of a product to be added.

        :type price: double
        :param price: The price of a product to be added.
        
        :return: An array containing the results of running get_title_bb & get_price_bb
        """
        if not re.search("www.bestbuy.com/", my_url):
            return [None, None]
        page_source = Scraper.__get_source(my_url)
        if page_source is not None and not isinstance(page_source, int):
            if title is None:
                title = Scraper.__get_title_bb(page_source)
            if price is None:
                price = Scraper.__get_price_bb(page_source)
            return [title, price]
        return [None, None]

    @staticmethod
    def get_fields_ne(my_url, title, price):
        """
        Retrieves the name of a product, and a product's price from a newegg link.

        :type my_url: string
        :param my_url: the newegg url of a product

        :type title: string
        :param title: The name of a product to be added.

        :type price: double
        :param price: The price of a product to be added.
        
        :return: An array containing the results of running get_title_ne & get_price_ne
        """
        if not re.search("www.newegg.com/", my_url):
            return [None, None]
        page_source = Scraper.__get_source(my_url)
        if page_source is not None and not isinstance(page_source, int):
            if title is None:
                title = Scraper.__get_title_ne(page_source)
            if price is None:
                price = Scraper.__get_price_ne(page_source)
            return [title, price]
        return [None, None]

    @staticmethod
    def get_fields_bh(my_url, title, price):
        """
        Retrieves the name of a product, and a product's price from a b&h link.

        :type my_url: string
        :param my_url: the b&h url of a product

        :type title: string
        :param title: The name of a product to be added.

        :type price: double
        :param price: The price of a product to be added.
        
        :return: An array containing the results of running get_title_bh & get_price_bh
        """
        if not re.search("/www.bhphotovideo.com/", my_url):
            return [None, None]
        page_source = Scraper.__get_source(my_url)
        if page_source is not None and not isinstance(page_source, int):
            if title is None:
                title = Scraper.__get_title_bh(page_source)
            if price is None:
                price = Scraper.__get_price_bh(page_source)
            return [title, price]
        return [None, None]

    @staticmethod
    def __get_title_bh(soup):
        """
        Retrieves the title of a product from a BS4 object that was generated from a B&H URL.
        
        :type soup: bs4-object
        :param soup: a bs4 object containing web-source code 
        
        :return: The title of a product or NONE if title is not found
        """
        results = soup.find(class_='title_1S1JLm7P93Ohi6H_hq7wWh')
        if results is None:
            print("ERROR title not found. Cannot add product.")
            print(
                'B&H bot detection may have picked you up. Please increase product checking interval in the '
                'scheduler. Then go to B&H\'s website to do their recaptcha and try again.')
            return None
        title = results.get_text().split('BH')[0]
        return title

    @staticmethod
    def __get_price_bh(soup):
        """
        Retrieves the price of a product from a BS4 object that was generated from a B&H URL.
        
        :type soup: bs4-object
        :param soup: a bs4 object containing web-source code 
        
        :return: The price of a product or NONE if the price is not found
        """
        results = soup.find(class_='price_1DPoToKrLP8uWvruGqgtaY')
        if results is None:
            print("ERROR price not found. Cannot add product.")
            return None
        price_str = results.get_text()
        price = float(price_str.split('$')[1].replace(',', ''))
        return price

    @staticmethod
    def __get_title_ne(soup):
        """
        Retrieves the title of a product from a BS4 object that was generated from a Newegg URL.
        
        :type soup: bs4-object
        :param soup: a bs4 object containing web-source code 
        
        :return: The title of a product or NONE if title is not found
        """
        results = soup.find(class_='product-title')
        if results is None:
            print("ERROR title not found. Cannot add product.")
            return None
        title = str(results)[len('<h1 class=\"product-title\">'):-len('</h1>')]
        return title

    @staticmethod
    def __get_price_ne(soup):
        """
        Retrieves the price of a product from a BS4 object that was generated from a Newegg URL.
        
        :type soup: bs4-object
        :param soup: a bs4 object containing web-source code 
        
        :return: The price of a product or NONE if price is not found
        """
        results = soup.find(class_='product-price')
        if results is None:
            print("ERROR price not found. Cannot add product.")
            return None
        price_str = results.get_text()
        print(price_str)
        if re.search('may or may not be restocked.', price_str):
            return None
        if not re.search('Sale', price_str):
            price = float(price_str.split('$')[1].replace(',', ''))
            return price

        if price_str is not None:
            price = re.findall(r"\d+\.\d+", price_str)
            # price = re.findall("d+.d+", price_str)
            if price is None:
                print("ERROR price not found. Cannot add product.")
                return None
            return float(price[0])
        return None

    @staticmethod
    def __get_title_bb(soup):
        """
        Retrieves the title of a product from a BS4 object that was generated from a Bestbuy URL.
        
        :type soup: bs4-object
        :param soup: a bs4 object containing web-source code 
        
        :return: The title of a product or NONE if title is not found
        """
        results = soup.find(class_='sku-title')
        if results is None:
            print("ERROR title not found. Cannot add product.")
            return None
        results = results.find(class_='heading-5 v-fw-regular')
        if results is None:
            print("ERROR title not found. Cannot add product.")
            return None
        title = str(results)[len('h1 class = \"heading-5 v-fw-regular\"'):-len('</h1>')]
        return title

    @staticmethod
    def __get_price_bb(soup):
        """
        Retrieves the title of a product from a BS4 object that was generated from a Bestbuy URL.
        
        :type soup: bs4-object
        :param soup: a bs4 object containing web-source code 
        
        :return: The price of a product or NONE if price is not found
        """
        results = soup.find(class_='priceView-hero-price priceView-customer-price')
        if results is None:
            print("ERROR price not found. Cannot add product.")
            return None
        price_str = str(results)
        price = float(price_str[price_str.index('aria-hidden="true">') + len('aria-hidden="true">') + 1:price_str.index(
            '</span><span class')].replace(',', ''))
        return price

    def __init__(self, url, url_type):
        """
        Instantiates a web scraper and pulls initial page source information.
        
        :type url: string
        :param url: The url of a link that will be scraped to find product information
        
        :type url_type: string
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
        """
        Finds and removes all metacharacters from the input string.

        :type results: string
        :param results: An input string that may or may not contain metacharacters

        :return: A string the same as the input string except that each
        metacharacter is replaced by a space
        """
        if results is not None:
            meta_char_list = [".", "^", "$", "+", "?", "{", "}", "[", "]", "\\", "|", "(", ")", "\t", "\n"]

            for i in meta_char_list:
                results = results.replace(i, " ")

            self.soup = results
        else:
            print("WARNING NONE RESULTS")
        return results

    def get_bb(self):
        """
        Searches for whether or not the HTML source grabbed by the scraper contains a product available for purchase with BestBuy 

        :return: 0 if the product is not found available for purchase. 
        :return: 1 if the product is found and available for purchase.
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
        Searches for whether or not the HTML source grabbed by the scraper contains a product available for purchase with B&H 

        :return: 0 if the product is not found available for purchase. 
        :return: 1 if the product is found and available for purchase.
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
        Searches for whether or not the HTML source grabbed by the scraper contains a product available for purchase with Newegg 

        :return: 0 if the product is not found available for purchase. 
        :return: 1 if the product is found and available for purchase.
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
