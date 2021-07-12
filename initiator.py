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

    def __init__(self, the_products):
        """"" Instantiates a class of type 'initiator' :param the_products: is the filename of where the properly
        formatted JSON file containing URL information is located "" """
        self.prodLink = the_products
        default_browser = ''
        self.set_default_browser()
        self.data = None
        print(self.prodLink)

    def set_default_browser(self):
        """
        Ensures that the default browser is set.
        :return: The first line in the file that is opened (which is the default browser)
        """
        try:
            with open('defaultBrowser.txt') as fp:
                self.default_browser = fp.readline()
        except:
            print("The 'defaultBrowser.txt' file could not be found")

    @staticmethod
    def poll_site(base_url):
        """
        Pings a website to see if the website is 'up'
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
        if 'Product' not in self.data:
            print("Invalid JSON, or the object is empty")
            return 0
        the_processes = []
        the_data = []
        num_crawled = 0
        for URL in self.data['Product']:

            url_str = str(URL['productLink'])
            print('running for ' + url_str)
            if re.search("www.bestbuy.com/", url_str) and self.poll_site("www.bestbuy.com"):
                the_processes.append(
                    subprocess.Popen(["python3", "scraper.py", URL['productLink'], 'BB', self.default_browser]))
                the_data.append([URL['productType'], url_str, URL['productPrice'], False])
            if re.search("www.newegg.com/", url_str) and self.poll_site("www.newegg.com"):
                the_processes.append(
                    subprocess.Popen(["python3", "scraper.py", URL['productLink'], 'NE', self.default_browser]))
                the_data.append([URL['productType'], url_str, URL['productPrice'], False])
            if re.search("www.bhphotovideo.com/", url_str) and self.poll_site("www.newegg.com"):
                the_processes.append(
                    subprocess.Popen(["python3", "scraper.py", URL['productLink'], 'BH', self.default_browser]))
                the_data.append([URL['productType'], url_str, URL['productPrice'], False])

            while len(the_processes) > 2:
                count = 0
                for p in the_processes:
                    if p.poll() == 0:
                        the_data.pop(count)
                        the_processes.pop(count)
                        num_crawled = num_crawled + 1
                    elif p.poll() == 1:
                        the_processes.pop(count)
                        interface.notification(the_data[count][0], the_data[count][1], the_data[count][2],
                                               the_data[count][3])
                        the_data.pop(count)
                        print('Interface call!!!!!')
                        num_crawled = num_crawled + 1
                    elif p.poll() == 2:
                        the_processes.pop(count)
                        the_data.pop(count)
                        print('Network Error')
                        num_crawled = num_crawled + 1
                    count = count + 1
        return num_crawled


if __name__ == '__main__':
    gotime = initiator(the_products="productList.json")
    print(gotime.initiate())
    exit()
