"""
This file handles the adding, and deleting of items from the productList.JSON file.
"""

import json
import re
import sys

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FFOpt

import initiator


class itemBase:
    """
    This class handles the modification of items inside of a designated productList.
    """

    def add_item(self, url, json_file_name):
        """
        Adds an item to the designated product list as a JSON entry. First it checks a URL for product information, then
        it adds corresponding price, and URL information to the productList.
        :param url: The URL of the item that needs to be monitored (B&H, Newegg, and Bestbuy links only)
        :param json_file_name: The productList that the URL's JSON entry will be placed in.
        :return: -5 if there is a duplicate link found within the JSON file.
        :return: -4 if the URL entered is not supported.
        :return: -3 if the URL's domain cannot be reached.
        :return: -2 if there is a problem opening the JSON file or Reading from it.
        :return: -1 if the item cannot be found.
        :return:  0 if the item could not be added to the json_file.
        :return:  1 if the item was added successfully.
        """
        if not initiator.pollSite(url):
            return -3
        try:
            with open(json_file_name, "r") as dataFile:
                data = json.load(dataFile)
        except:
            print("Something went wrong with loading the JSON file.")
            return -1
        if 'Product' in data:
            for URLStr in data['Product']:
                if str(URLStr['productLink']) == url:
                    print("Duplicate URL, cannot add.")
                    return -5
        print("Adding URL...")

        the_driver = './drivers/geckodriver'
        option = FFOpt()
        option.headless = True
        browser = webdriver.Firefox(options=option, executable_path=the_driver)
        browser.get(url)
        title = ' '
        price = ' '
        soup = BeautifulSoup(browser.page_source, 'html.parser')
        browser.close()
        if re.search("www.bestbuy.com/", url):
            results = soup.find(class_='sku-title')
            if results is None:
                print("ERROR title not found. Cannot add product.")
                return -1
            results = results.find(class_='heading-5 v-fw-regular')
            if results is None:
                print("ERROR title not found. Cannot add product.")
                return -1
            title = str(results)[len('h1 class = \"heading-5 v-fw-regular\"'):-len('</h1>')]
            print('Item is called ' + title)
            results = soup.find(class_='priceView-hero-price priceView-customer-price')
            if results is None:
                print("ERROR price not found. Cannot add product.")
                return -1
            price_str = str(results)
            price = float(price_str[
                          price_str.index('aria-hidden="true">') + len('aria-hidden="true">') + 1:price_str.index(
                              '</span><span class')].replace(',', ''))
            print('The price is ' + str(price))

        elif re.search("www.newegg.com/", url):
            results = soup.find(class_='product-title')
            if results is None:
                print("ERROR title not found. Cannot add product.")
                return -1
            title = str(results)[len('<h1 class=\"product-title\">'):-len('</h1>')]
            print(title)
            results = soup.find(class_='product-price')
            if results is None:
                print("ERROR price not found. Cannot add product.")
                return -1
            price_str = results.get_text()
            if re.search('Sale', price_str):
                price = re.findall("\d+\.\d+", price_str)
                if price is None:
                    print("ERROR price not found. Cannot add product.")
                    return -1
                price = float(price[0])
                print(str(price))
            else:
                price = float(price_str.split('$')[1].replace(',', ''))

        elif re.search("www.bhphotovideo.com", url):
            results = soup.find(class_='title_1S1JLm7P93Ohi6H_hq7wWh')
            if results is None:
                print("ERROR title not found. Cannot add product.")
                print(
                    'B&H bot detection may have picked you up. Please increase product checking interval in the '
                    'scheduler. Then go to B&H\'s website to do their recaptcha and try again.')
                return -1
            title = results.get_text().split('BH')[0]
            print("The title is " + title)
            results = soup.find(class_='price_1DPoToKrLP8uWvruGqgtaY')
            if results is None:
                print("ERROR price not found. Cannot add product.")
                return -1
            price_str = results.get_text()
            price = float(price_str.split('$')[1].replace(',', ''))
            print(price)
        else:
            print("The text which was input is not supported")
            browser.close()
            return -4

        browser.close()
        return self.add_json(title, url, price)

    @staticmethod
    def add_json(title, url, price, json_file_name):
        """
        Adds JSON to a designated JSON file
        :param title: The title of the item to be added to the JSON
        :param url: The URL of the item to be added to the JSON
        :param price: The price of the item to be added to the JSON
        :param json_file_name: The JSON file to add the product to
        :return: 0 if an error occurred when writing the JSON
        :return: 1 if the JSON was added successfully.
        """
        try:
            with open(json_file_name, "r") as dataFile:
                data = json.load(dataFile)
            json_obj = {'productType': title, 'productLink': url, 'productPrice': price}
            data['Product'].append(json_obj)
            dataFile = open('productList.json', 'w+')
            dataFile.seek(0)

            json.dump(data, dataFile)
            dataFile.truncate()
            dataFile.close()
            return 1
        except:
            print("An Error occurred while writing to JSON")
            return 0

    @staticmethod
    def del_item(url, json_file_name):
        """
        Deletes a specified JSON entry from a specified json_file by URL
        :param url: The URL of the item to be deleted.
        :param json_file_name: The file to delete the JSON entry from.
        :return: 0 if an error occurred when trying to delete the entry.
        :return: 1 if the item was deleted successfully.
        """
        try:
            with open(json_file_name, 'r') as json_file_name:
                data = json.load(json_file_name)

            index = 0
            found = 0
            for url_str in data['Product']:
                if str(url_str['productLink']) == url:
                    found = 1
                    break
                index += 1

            if found == 0:
                return print('No item found at this URL')

            item = data['Product'].pop(index)

            data_file = open(json_file_name, 'w+')
            data_file.seek(0)

            json.dump(data, data_file, indent=4)
            data_file.truncate()
            data_file.close()

            return 1
        except:
            print("An error has occured when attempting to delete from the JSON file.")
            return 0


if __name__ == '__main__':
    if len(sys.argv) == 3:
        execution_type = sys.argv[1]
        URL = sys.argv[2]
        json_file = sys.argv[3]
        json_file = 'productList.json'
        if execution_type == 1:
            itemBase().add_item(URL, json_file)
        elif execution_type == 2:
            itemBase.del_item(json_file)
    else:
        print(
            "Syntax is incorrect, please run again with this format:\npython3 itemBase.py <1/2> <URL> <JSON FILE "
            "NAME>\n 1 - for additions\n 2 - for deletions") 
