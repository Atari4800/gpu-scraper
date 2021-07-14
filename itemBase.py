"""
This file handles the adding, and deleting of items from the productList.JSON file.
"""

import json, sys, re
import initiator
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options as FFOpt
from bs4 import BeautifulSoup




class itemBase:
    """
    This class handles the modification of items inside of a designated productList.
    """
    def addItem(self, URL, json_file):
        """
        Adds an item to the designated product list as a JSON entry. First it checks a URL for product information, then
        it adds corresponding price, and URL information to the productList.
        
        :type URL: string
        :param URL: The URL of the item that needs to be monitored (B&H, Newegg, and Bestbuy links only)
        
        :type json_file: string
        :param json_file: The productList that the URL's JSON entry will be placed in.
        :return: -5 if there is a duplicate link found within the JSON file.
        :return: -4 if the URL entered is not supported.
        :return: -3 if the URL's domain cannot be reached.
        :return: -2 if there is a problem opening the JSON file or Reading from it.
        :return: -1 if the item cannot be found.
        :return:  0 if the item could not be added to the json_file.
        :return:  1 if the item was added successfully.
        """
        if not initiator.pollSite(URL) :
            return -3
        try:
            with open(json_file, "r") as dataFile:
                data = json.load(dataFile)
        except:
            print("Something went wrong with loading the JSON file.")
            return -1
        if 'Product' in data :
            for URLStr in data['Product']:
                if str(URLStr['productLink']) == URL :
                    print("Duplicate URL, cannot add.")
                    return -5
        print("Adding URL...")

        theDriver = './drivers/geckodriver'
        option = FFOpt()
        option.headless = True
        browser = webdriver.Firefox(options=option, executable_path=theDriver)
        browser.get(URL)
        title = ' '
        price = ' '
        soup = BeautifulSoup(browser.page_source,'html.parser')
        browser.close()
        if re.search("www.bestbuy.com/", URL) :
            results = soup.find(class_ = 'sku-title')
            if results == None:
                print ("ERROR title not found. Cannot add product.")
                return -1
            results = results.find(class_ = 'heading-5 v-fw-regular')
            if results == None:
                print ("ERROR title not found. Cannot add product.")
                return -1
            title=str(results)[len('h1 class = \"heading-5 v-fw-regular\"'):-len('</h1>')]
            print('Item is called ' +title)
            results = soup.find(class_ = 'priceView-hero-price priceView-customer-price')
            if results == None:
                print ("ERROR price not found. Cannot add product.")
                return -1
            priceStr=str(results)
            price=float(priceStr[priceStr.index('aria-hidden="true">') + len('aria-hidden="true">') +1:priceStr.index('</span><span class')].replace(',',''))
            print('The price is ' + str(price))

        elif re.search("www.newegg.com/",URL) :
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
            priceStr=results.get_text()
            if re.search('Sale',priceStr) :
                price = re.findall("\d+\.\d+",priceStr)
                if price == None:
                    print("ERROR price not found. Cannot add product.")
                    return -1
                price = float(price[0])
                print(str(price))
            else:
                price=float(priceStr.split('$')[1].replace(',',''))

        elif re.search("www.bhphotovideo.com",URL) :
            results = soup.find(class_ = 'title_1S1JLm7P93Ohi6H_hq7wWh')
            if results == None:
                print ("ERROR title not found. Cannot add product.")
                print('B&H bot detection may have picked you up. Please increase product checking interval in the scheduler. Then go to B&H\'s website to do their recaptcha and try again.')
                return -1
            title=results.get_text().split('BH')[0]
            print("The title is "+title)
            results = soup.find(class_ = 'price_1DPoToKrLP8uWvruGqgtaY')
            if results == None:
                print ("ERROR price not found. Cannot add product.")
                return -1
            priceStr=results.get_text()
            price = float(priceStr.split('$')[1].replace(',',''))
            print(price)
        else:
            print("The text which was input is not supported")
            browser.close()
            return -4

        browser.close()
        return self.addJSON(title, URL, price)



    def addJSON(self, title, URL, price, json_file):
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
            with open(json_file, "r") as dataFile:
                data = json.load(dataFile)
            jsonObj = {'productType':title,'productLink':URL,'productPrice':price}
            data['Product'].append(jsonObj)
            dataFile = open('productList.json','w+')
            dataFile.seek(0)

            json.dump(data,dataFile)
            dataFile.truncate()
            dataFile.close()
            return 1
        except:
            print("An Error occurred while writing to JSON")
            return 0

    def delItem(self, url, json_file):
        """
        Deletes a specified JSON entry from a specified json_file by URL
        
        :type url: string
        :param url: The URL of the item to be deleted.
        
        :type json_file: string
        :param json_file: The file to delete the JSON entry from.
        
        :return: 0 if an error occurred when trying to delete the entry.
        :return: 1 if the item was deleted successfully.
        """
        try:
            with open(json_file, 'r') as json_file:
                data = json.load(json_file)

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

            dataFile = open(json_file, 'w+')
            dataFile.seek(0)

            json.dump(data, dataFile, indent=4)
            dataFile.truncate()
            dataFile.close()

            return 1
        except:
            print("An error has occured when attempting to delete from the JSON file.")
            return 0

if __name__ == '__main__':
    if len(sys.argv) == 3 :
        type = sys.argv[1]
        URL = sys.argv[2]
        json_file = sys.argv[3]
        json_file = 'productList.json'
        if type == 1:
            itemBase().addItem(URL, json_file)
        elif type == 2:
            itemBase.delItem(URL, json_file)
    else :
        print("Syntax is incorrect, please run again with this format:\npython3 itemBase.py <1/2> <URL> <JSON FILE NAME>\n 1 - for additions\n 2 - for deletions")
