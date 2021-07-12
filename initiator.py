"""
This file handles the 'main' for the backend of the gpu-scraper application.
It is able to ping hosts, and controls how a productList is searched through for content.
"""

import subprocess
import re
import json
import platform
import interface


class initiator:
    """
    This class handles the instantiation of a productList and has the ability to test sites and products
    """
    def __init__(self, theProducts):
        """""
        Instantiates a class of type 'initiator'
        :param theProducts: is the filename of where the properly formatted JSON file containing URL information is located
        """""
        self.prodLink = theProducts
        defaultBrowser = ''
        self.setDefaultBrowser()
        self.data = None
        print(self.prodLink)

    def setDefaultBrowser(self):
        """
        Ensures that the default browser is set.
        :return: The first line in the file that is opened (which is the default browser)
        """
        try:
            with open('defaultBrowser.txt') as fp:
                self.defaultBrowser = fp.readline()
        except:
            print("The 'defaultBrowser.txt' file could not be found")



    def pollSite(self,baseURL):
        """
        Pings a website to see if the website is 'up'
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
        Begins the backend portion of the program, loads the JSON file and reads for the URLs therein.
        If the URL contains one of the supported link websites, then it calls the appropriate subprocess to attempt to
        find product in the URL
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

            while len(theProcesses) > 2:
                count = 0 
                for p in theProcesses :
                    if p.poll() == 0:
                        theData.pop(count)
                        theProcesses.pop(count)
                        numCrawled = numCrawled + 1
                    elif p.poll() == 1:
                        theProcesses.pop(count)
                        interface.notification(theData[count][0],theData[count][1],theData[count][2],theData[count][3])
                        theData.pop(count)
                        print('Interface call!!!!!')
                        numCrawled = numCrawled + 1
                    elif p.poll() == 2:
                        theProcesses.pop(count)
                        theData.pop(count)
                        print('Network Error')
                        numCrawled = numCrawled + 1
                    count = count + 1
        return numCrawled


if __name__ == '__main__':
    gotime = initiator(theProducts="productList.json")
    print(gotime.initiate())
    exit()
