"""
This file handles the 'main' for the backend of the gpu-scraper application. It is able to ping hosts, and controls how a productList is searched through for content.
"""

import subprocess
import re
import json
import platform
import interface

from datetime import datetime

from item_base import item_base as item_base


class Initiator:

    """
    This class handles the instantiation of a productList and has the ability to test sites and products
    """
    def __init__(self, theProducts):
        """
        Instantiates a class of type 'initiator'
        
        :type theProducts: string
        :param theProducts: is the filename of where the properly formatted JSON file containing URL information is located
        """
        self.prodLink = theProducts
        defaultBrowser = ''
        self.setDefaultBrowser()
        self.data = None
        print(self.prodLink)
        self.maxProcesses = 2

    def setDefaultBrowser(self):
        """
        Ensures that the default browser is set.
        
        :return: The first line in the file that is opened (which is the default browser)
        """
        try:
            with open('defaultBrowser.txt') as fp:
                self.defaultBrowser = fp.readline().strip('\n')
        except:
            print("The 'defaultBrowser.txt' file could not be found")


    @staticmethod
    def pollSite(baseURL):
        """
        Pings a website to see if the website is 'up'
        
        :type baseURL: string
        :param baseURL: The website to be pinged
        
        :return: The number of successful pings to the target website
        """
        host = re.search(r'//(.*?)/',baseURL)
        if host != None:
            host = host.group(1)
        else:
            host = baseURL
        print("Checking if the Host is up! ")
        # Option for the number of packets as a function of
        p_type = '-n' if platform.system().lower() == 'windows' else '-c'
        w_type = '-t' if platform.system().lower() == 'windows' else '-w'

        # Building the command. Ex: "ping -c 1 google.com"
        command = ['ping', p_type, '1', w_type, '1', host]
        return subprocess.call(command) == 0

    def initiate(self):
        """

        Begins the backend portion of the program, loads the JSON file and reads for the urls therein. If the url
        contains one of the supported link websites, then it calls the appropriate subprocess to attempt to find
        product in the url. If a product is found/not found isAvailable is updated accordingly. If a product is
        found then lastAvailable is updated with the current date/time.

        
        :return: The number of websites that were crawled.
        """
        print('initiated')
        print('Attempting to open JSON file.')
        try:
            with open(self.prodLink, "r") as data_file:
                self.data = json.load(data_file)
        except:
            print("The JSON file could either not be found, or not be opened. Please check that it exists.")
            return 0
        print('Checking JSON content.')
        if not 'Product' in self.data:
            print("Invalid JSON, or the object is empty")
            return 0
        theProcesses=[]
        theData = []
        numCrawled = 0
        prodcnt = 0
        sizeofdata = int(len(self.data['Product']))
        print(len(self.data['Product']))
        for URL in self.data['Product']:
            URLstr=str(URL['productLink'])
            print('running for ' + URLstr)
            if re.search("www.bestbuy.com/", URLstr) and self.pollSite("www.bestbuy.com"):

                theProcesses.append(subprocess.Popen(["python3", "scraper.py", URL['productLink'], 'BB', self.defaultBrowser]))
                theData.append([URL['productType'],URLstr,URL['productPrice'],False])
            if re.search("www.newegg.com/", URLstr) and self.pollSite("www.newegg.com"):
                theProcesses.append(subprocess.Popen(["python3", "scraper.py", URL['productLink'], 'NE', self.defaultBrowser]))
                theData.append([URL['productType'], URLstr, URL['productPrice'], False])
            if re.search("www.bhphotovideo.com/", URLstr) and self.pollSite("www.newegg.com"):
                theProcesses.append(subprocess.Popen(["python3", "scraper.py", URL['productLink'], 'BH', self.defaultBrowser]))
                theData.append([URL['productType'], URLstr, URL['productPrice'], False])
            prodcnt = prodcnt + 1
            if len(theProcesses) > self.maxProcesses or prodcnt >= sizeofdata-self.maxProcesses:
                while len(theProcesses) != 0:
                    count = 0
                    for p in theProcesses :
                        if p.poll() == 0:

                            for prod in self.data['Product']:
                                if re.search(prod['productLink'], the_data[count][1]):
                                    prod['isAvailable'] = False
                                    prod['lastAvailable'] = prod['lastAvailable']
                            the_data.pop(count)
                            the_processes.pop(count)
                            num_crawled += 1

                        elif p.poll() == 1:
                            the_processes.pop(count)
                            for prod in self.data['Product']:
                                if re.search(prod['productLink'], the_data[count][1]):
                                    prod['isAvailable'] = True
                                    now = datetime.now()
                                    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
                                    prod['lastAvailable'] = dt_string
                            interface.notification(the_data[count][0],the_data[count][1],the_data[count][2],the_data[count][3])
                            the_data.pop(count)
                            print('Interface call!!!!!')
                            num_crawled += 1
                        count += 1
            item_base.save_state(self.data, self.prod_link)
        return num_crawled



if __name__ == '__main__':
    gotime = initiator(theProducts="productList.json")
    print(gotime.initiate())
    exit(33)
