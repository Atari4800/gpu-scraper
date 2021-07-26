"""
This file handles the adding, and deleting of items from the productList.JSON file.
"""

import json, sys, re
import initiator
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options as FFOpt
from bs4 import BeautifulSoup

import scraper


class item_base:
    """
    This class handles the modification of items inside of a designated productList.
    """


    def add_item(self, url, title, price, json_file):

        """
        Adds an item to the designated product list as a JSON entry. First it checks a url for product information, then
        it adds corresponding price, and url information to the productList.
        
        :type url: string
        :param url: The url of the item that needs to be monitored (B&H, Newegg, and Bestbuy links only)
        
        :type json_file: string
        :param json_file: The productList that the url's JSON entry will be placed in.
        :return: -5 if there is a duplicate link found within the JSON file.
        :return: -4 if the url entered is not supported.
        :return: -3 if the url's domain cannot be reached.
        :return: -2 if there is a problem opening the JSON file or Reading from it.
        :return: -1 if the item cannot be found.
        :return:  0 if the item could not be added to the json_file.
        :return:  1 if the item was added successfully.
        """






        pinger = initiator.Initiator
        if not pinger.poll_site(base_url=url):
            return -3
        supported_urls = ['www.bestbuy.com/', 'www.newegg.com/', 'www.bestbuy.com/']
        if not any(x in url for x in supported_urls):
            return -4
        try:
            with open(json_file, "r") as data_file:
                data = json.load(data_file)
        except:
            print("Something went wrong with loading the JSON file.")
            return -2
        if 'Product' in data:
            for url_str in data['Product']:
                if str(url_str['productLink']) == url:
                    print("Duplicate url, cannot add.")
                    return -5

        print("Attemping to add url and its information...")
        if title is None or price is None:
            if re.search("www.bestbuy.com/", url):
                fields = scraper.get_fields_bb(url,title,price)
            elif re.search("www.newegg.com/"):
                fields = scraper.get_fields_ne(url,title,price)
            elif re.search("www.bhphotovideo.com", url) :
                fields = scraper.get_fields_bh(url,title,price)
            else:
                print("The text which was input is not supported")
                return -4
            title = fields[0]
            price = fields[1]
        print(url)
        print(title)
        print(price)
        if title is None or price is None:
            return -1
        data_file.close()
        return self.add_json(title, url, price, json_file)


    @staticmethod
    def add_json(title, url, price, json_file):
        """
        Adds JSON to a designated JSON file
        
        :type title: string
        :param title: The title of the item to be added to the JSON
        
        :type url: string
        :param url: The url of the item to be added to the JSON
        
        :type price: string
        :param price: The price of the item to be added to the JSON
        
        :type json_file: string
        :param json_file: The JSON file to add the product to
        
        :return: 0 if an error occurred when writing the JSON
        :return: 1 if the JSON was added successfully.
        """
        try:
            with open(json_file, "r") as data_file:
                data = json.load(data_file)
            with open(json_file, "r") as data_file:
                dupData = json.load(data_file)
            json_obj = {'productType':title,'productLink':url,'productPrice':price}
            data['Product'].append(json_obj)

            data_file = open('productList.json', 'w+')
            data_file.seek(0)

            json.dump(data, data_file)
            data_file.truncate()
            data_file.close()
            with open(json_file, "r") as data_file:
                data2 = json.load(data_file)
            if dupData == data2:
                print("An Error occurred while writing to JSON")
                return 0
            else:
                return 1
        except:
            print("An Error occurred while opening/writing to JSON")
            return 0

    def del_item(self, url, json_file):
        """
        Deletes a specified JSON entry from a specified json_file by url

        
        :type url: string
        :param url: The url of the item to be deleted.
        
        :type json_file: string

        :param json_file: The file to delete the JSON entry from.
        
        :return: 0 if an error occurred when trying to delete the entry.
        :return: 1 if the item was deleted successfully.
        """
        try:
            with open(json_file, 'r') as json_file:
                data = json.load(json_file)

            index = 0
            found = None
            for url_str in data['Product']:
                print(url_str['productLink'])
                if url == data['Product']['productLink']:
                    found = data['Product'].pop(index)
                index += 1

            if found is None:
                return 0
            #item = data['Product'].pop(index)
            data_file = open(json_file, 'w+')
            data_file.seek(0)
            json.dump(data, data_file)
            data_file.truncate()
            data_file.close()

            return 1
        except:
            print("An error has occured when attempting to delete from the JSON file.")
            return 0

if __name__ == '__main__':
    if len(sys.argv) == 3 :
        type = sys.argv[1]
        urlz = sys.argv[2]
        #json_file = sys.argv[3]
        jsonfile = 'productList.json'
        if type == '1':
            print("Adding Item")
            item_base().add_item(urlz, jsonfile)
        elif type == '2':
            item_base().del_item(url=urlz, json_file=jsonfile)
    else :
        print("Syntax is incorrect, please run again with this format:\npython3 item_base.py <1/2> <url> <JSON FILE NAME>\n 1 - for additions\n 2 - for deletions")
