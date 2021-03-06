"""
This file handles the adding, and deleting of items from the productList.JSON file.
"""

import json
import platform
import re
import subprocess
import sys

import scraper


class item_base:
    """
    This class handles the modification of items inside of a designated productList.
    """

    def __poll_site(base_url):
        """
        This is the same method from initiator, it has been added to prevent circular dependencies.
            Pings a website to see if the website is 'up'

        :type base_url: string
        :param base_url: The website to be pinged

        :return: The number of successful pings to the target website
        """
        host = re.search(r'//(.*?)/', base_url)
        if host is not None:
            host = host.group(1)
        else:
            host = base_url
        print("Checking if the Host is up! ")
        # Option for the number of packets as a function of
        p_type = '-n' if platform.system().lower() == 'windows' else '-c'
        w_type = '-t' if platform.system().lower() == 'windows' else '-w'

        # Building the command. Ex: "ping -c 1 google.com"
        command = ['ping', p_type, '1', w_type, '1', host]
        return subprocess.call(command) == 0

    @staticmethod
    def add_item(url, title, price, json_file):
        """
        Adds an item to the designated product list as a JSON entry. First it checks a URL for product information, then
        it adds corresponding price, and URL information to the productList.


        :type url: string
        :param url: The url of the item that needs to be monitored (B&H, Newegg, and Bestbuy links only)

        :type title: string
        :param title: The name of a product to be added.

        :type price: double
        :param price: The price of a product to be added.


        :type json_file: string
        :param json_file: The productList that the URL's JSON entry will be placed in.
        :return: -6 if the price cannot be found.
        :return: -5 if there is a duplicate link found within the JSON file.
        :return: -4 if the URL entered is not supported.
        :return: -3 if the URL's domain cannot be reached.
        :return: -2 if there is a problem opening the JSON file or Reading from it.
        :return: -1 if the item cannot be found.
        :return:  0 if the item could not be added to the file.
        :return:  1 if the item was added successfully.
        """

        if not item_base.__poll_site(base_url=url):
            return -3
        supported_urls = ['www.bestbuy.com/', 'www.newegg.com/', 'www.bhphotovideo.com/']
        if not any(x in url for x in supported_urls):
            return -4
        try:
            with open(json_file, "r") as data_file:
                data = json.load(data_file)
        except Exception:
            print("Something went wrong with loading the JSON file.")
            return -2

        if 'Product' in data:
            for url_str in data['Product']:
                if str(url_str['productLink']) == url:
                    print(str(url_str['productLink']))
                    print("Duplicate url, cannot add.")
                    return -5

        print("Attemping to add url and its information...")
        if title is None or price is None:
            if re.search("www.bestbuy.com/", url):
                fields = scraper.Scraper.get_fields_bb(url, title, price)
            elif re.search("www.newegg.com/", url):
                fields = scraper.Scraper.get_fields_ne(url, title, price)
            elif re.search("www.bhphotovideo.com", url):
                fields = scraper.Scraper.get_fields_bh(url, title, price)
            else:
                print("The text which was input is not supported")
                return -4
            title = fields[0]
            price = fields[1]
        if title is None:
            return -1
        if price is None:
            return -6
        print(url)
        print(title)
        print(price)

        data_file.close()
        return item_base.__add_json(title, url, price, json_file)

    @staticmethod
    def save_state(data, json_file):
        """
        Saves json data to a particular datafile.

        :type data: List/Dict
        :param data: a list or dictionary containing JSON information that needs to be saved.

        :type json_file: string
        :param json_file: The name of a json_file to save information to.
        """
        try:
            data_file = open(json_file, 'w+')
            data_file.seek(0)
            data_file.write(json.dumps(data, sort_keys=True, indent=4, separators=(',', ':')))
            data_file.truncate()

            data_file.close()
        except Exception:
            print("THE STATE COULD NOT BE SAVED")
            return 0
        return 1

    @staticmethod
    def __add_json(title, url, price, json_file):

        """
        Adds JSON to a designated JSON file

        :type title: string
        :param title: The title of the item to be added to the JSON

        :type URL: string
        :param URL: The URL of the item to be added to the JSON

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
            json_obj = {'productType': title, 'productLink': url, 'productPrice': price, 'isAvailable': False,
                        'lastAvailable': ""}
            data['Product'].append(json_obj)
            data_file.close()
            return item_base.save_state(data, json_file)
        except Exception:
            print("An Error occurred while opening/writing to JSON")
            return 0

    @staticmethod
    def del_item(url, json_file):

        """
        Deletes a specified JSON entry from a specified json_file by URL

        :type url: string

        :param url: The url of the item to be deleted.


        :type json_file: string
        :param json_file: The file to delete the JSON entry from.

        :return: 0 if an error occurred when trying to delete the entry.
        :return: 1 if the item was deleted successfully.
        """

        with open(json_file, 'r') as temp_file:
            data = json.load(temp_file)

        index = 0
        found = None
        for url_str in data['Product']:
            if url == url_str['productLink']:
                found = data['Product'].pop(index)
            index += 1

        if found is None:
            return 0

        with open(json_file, 'w') as dataFile:
            dataFile.seek(0)
            json.dump(data, dataFile, indent=4)

        return 1


if __name__ == '__main__':
    if len(sys.argv) == 3:
        running_type = sys.argv[1]
        URLz = sys.argv[2]
        # json_file = sys.argv[3]
        jsonfile = 'productList.json'
        if running_type == '1':
            print("Adding Item")
            item_base().add_item(URLz, title=None, price=None, json_file=jsonfile)
        elif running_type == '2':
            item_base().del_item(url=URLz, json_file=jsonfile)
    else:
        print(
            "Syntax is incorrect, please run again with this format:\npython3 itemBase.py <1/2> <URL> <JSON FILE "
            "NAME>\n 1 - for additions\n 2 - for deletions")
