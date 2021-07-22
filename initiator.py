"""This file handles the 'main' for the backend of the gpu-scraper application. It is able to ping hosts,
and controls how a productList is searched through for content. """

import subprocess
import re
import json
import platform


# import interface


class Initiator:
    """
    This class handles the instantiation of a productList and has the ability to test sites and products
    """

    def __init__(self, the_products):
        """
        Instantiates a class of type 'initiator'
        
        :type the_products: string :param the_products: is the filename of where the properly formatted JSON file
        containing url information is located
        """
        self.prod_link = the_products
        default_browser = ''
        self.set_default_browser()
        self.data = None
        print(self.prod_link)
        self.max_processes = 2

    def set_default_browser(self):
        """
        Ensures that the default browser is set.
        
        :return: The first line in the file that is opened (which is the default browser)
        """
        try:
            with open('default_browser.txt') as fp:
                self.default_browser = fp.readline().strip('\n')
        except Exception:
            print("The 'default_browser.txt' file could not be found")

    @staticmethod
    def poll_site(base_url):
        """
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

    def initiate(self):
        """
        Begins the backend portion of the program, loads the JSON file and reads for the urls therein. If the url
        contains one of the supported link websites, then it calls the appropriate subprocess to attempt to find
        product in the url
        
        :return: The number of websites that were crawled.
        """
        print('initiated')
        print('Attempting to open JSON file.')
        try:
            with open(self.prod_link, "r") as data_file:
                self.data = json.load(data_file)
        except Exception:
            print("The JSON file could either not be found, or not be opened. Please check that it exists.")
            return 0
        print('Checking JSON content.')
        if 'Product' not in self.data:
            print("Invalid JSON, or the object is empty")
            return 0
        the_processes = []
        the_data = []
        num_crawled = 0
        prod_count = 0
        data_size = len(self.data['Product'])
        print(len(self.data['Product']))
        for url in self.data['Product']:
            url_string_name = str(url['productLink'])
            print('running for ' + url_string_name)
            if re.search("www.bestbuy.com/", url_string_name) and self.poll_site("www.bestbuy.com"):
                the_processes.append(
                    subprocess.Popen(["python3", "scraper.py", url['productLink'], 'BB', self.default_browser]))
                the_data.append([url['productType'], url_string_name, url['productPrice'], False])
            if re.search("www.newegg.com/", url_string_name) and self.poll_site("www.newegg.com"):
                the_processes.append(
                    subprocess.Popen(["python3", "scraper.py", url['productLink'], 'NE', self.default_browser]))
                the_data.append([url['productType'], url_string_name, url['productPrice'], False])
            if re.search("www.bhphotovideo.com/", url_string_name) and self.poll_site("www.newegg.com"):
                the_processes.append(
                    subprocess.Popen(["python3", "scraper.py", url['productLink'], 'BH', self.default_browser]))
                the_data.append([url['productType'], url_string_name, url['productPrice'], False])
            prod_count += 1
            if len(the_processes) > self.max_processes or prod_count >= data_size - self.max_processes:
                while len(the_processes) != 0:
                    count = 0
                    for p in the_processes:
                        if p.poll() == 0:
                            the_data.pop(count)
                            the_processes.pop(count)
                            num_crawled += 1
                        elif p.poll() == 1:
                            the_processes.pop(count)
                            # interface.notification(the_data[count][0],the_data[count][1],the_data[count][2],the_data[count][3])
                            the_data.pop(count)
                            print('Interface call!!!!!')
                            num_crawled += 1
                        count += 1
        return num_crawled


if __name__ == '__main__':
    init_obj = Initiator(the_products="productList.json")
    print(init_obj.initiate())
    exit(0)
