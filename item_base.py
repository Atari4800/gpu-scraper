"""
This file handles the adding, and deleting of items from the productList.JSON file.
"""

import json, sys, re
import initiator
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options as FFOpt
from bs4 import BeautifulSoup




class item_base:
    """
    This class handles the modification of items inside of a designated productList.
    """
    def add_item(self, url, json_file):
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
        if not pinger.poll_site(base_url = url) :
            return -3
        try:
            with open(json_file, "r") as data_file:
                data = json.load(data_file)
        except:
            print("Something went wrong with loading the JSON file.")
            return -2
        if 'Product' in data :
            for url_str in data['Product']:
                if str(url_str['productLink']) == url :
                    print("Duplicate url, cannot add.")
                    return -5
        print("Adding url...")

        the_driver = './drivers/geckodriver'
        option = FFOpt()
        option.headless = True
        browser = webdriver.Firefox(options=option, executable_path=the_driver)
        browser.get(url)
        title = ' '
        price = ' '
        soup = BeautifulSoup(browser.page_source,'html.parser')
        browser.close()
        if re.search("www.bestbuy.com/", url) :
            results = soup.find(class_ = 'sku-title')
            if results == None:
                print ("ERROR title not found. Cannot add product.")
                return -1
            results = results.find(class_ = 'heading-5 v-fw-regular')
            if results == None:
                print ("ERROR title not found. Cannot add product.")
                return -1
            title = str(results)[len('h1 class = \"heading-5 v-fw-regular\"'):-len('</h1>')]
            print('Item is called ' + title)
            results = soup.find(class_ = 'priceView-hero-price priceView-customer-price')
            if results == None:
                print ("ERROR price not found. Cannot add product.")
                return -1
            price_str = str(results)
            price = float(price_str[price_str.index('aria-hidden="true">') + len('aria-hidden="true">') +1:price_str.index('</span><span class')].replace(',',''))
            print('The price is ' + str(price))

        elif re.search("www.newegg.com/",url) :
            results = soup.find(class_ = 'product-title')
            if results == None:
                print ("ERROR title not found. Cannot add product.")
                return -1
            title = str(results)[len('<h1 class=\"product-title\">'):-len('</h1>')]
            print(title)
            results = soup.find(class_ = 'product-price')
            if results == None:
                print ("ERROR price not found. Cannot add product.")
                return -1
            price_str = results.get_text()
            if re.search('Sale',price_str) :
                price = re.findall(r"\d+\.\d+", price_str)
                #price = re.findall("d+.d+", price_str)
                if price == None:
                    print("ERROR price not found. Cannot add product.")
                    return -1
                price = float(price[0])
                print(str(price))
            else:
                price = float(price_str.split('$')[1].replace(',',''))

        elif re.search("www.bhphotovideo.com", url) :
            results = soup.find(class_ = 'title_1S1JLm7P93Ohi6H_hq7wWh')
            if results is None:
                print ("ERROR title not found. Cannot add product.")
                print('B&H bot detection may have picked you up. Please increase product checking interval in the scheduler. Then go to B&H\'s website to do their recaptcha and try again.')
                return -1
            title = results.get_text().split('BH')[0]
            print("The title is "+title)
            results = soup.find(class_ = 'price_1DPoToKrLP8uWvruGqgtaY')
            if results == None:
                print ("ERROR price not found. Cannot add product.")
                return -1
            price_str = results.get_text()
            price = float(price_str.split('$')[1].replace(',',''))
            print(price)
        else:
            print("The text which was input is not supported")
            return -4
        print(url)
        print(title)
        print(price)
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
