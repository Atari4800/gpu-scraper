import subprocess
import re
import json

import interface


class initiator:
    def __init__(self):
        self.prodLink = "productList.json"
        self.defaultBrowser=''
        self.data = None
        print(self.prodLink)
    def setDefaultBrowser(self):
        with open('defaultBrowser.txt') as fp:
            self.defaultBrowser = fp.readline()


    def pollSite(baseURL):
        return(subprocess.run(["ping -c 1 " + baseURL]))

    def initiate(self):
        print('initiated')
        with open(self.prodLink, "r") as data_file:
                self.data = json.load(data_file)

        theProcesses=[]
        theData = []
        for URL in self.data['Product']:

            URLstr=str(URL['productLink'])
            print('running for ' + URLstr)
            if re.search("www.bestbuy.com/", URLstr) :
                theProcesses.append(subprocess.Popen(["python3", "scraper.py", URL['productLink'], 'BB', self.defaultBrowser]))
                theData.append([URL['productType'],URLstr,URL['productPrice'],False])
            if re.search("www.newegg.com/", URLstr) :
                theProcesses.append(subprocess.Popen(["python3", "scraper.py", URL['productLink'], 'NE', self.defaultBrowser]))
                theData.append([URL['productType'], URLstr, URL['productPrice'], False])
            if re.search("www.bhphotovideo.com/", URLstr) :
                theProcesses.append(subprocess.Popen(["python3", "scraper.py", URL['productLink'], 'BH', self.defaultBrowser]))
                theData.append([URL['productType'], URLstr, URL['productPrice'], False])

            while len(theProcesses) > 2:
                count = 0 
                for p in theProcesses :
                    if p.poll() == 0:
                        theData.pop(count)
                        theProcesses.pop(count)
                    elif p.poll() == 1:
                        theProcesses.pop(count)
                        interface.notification(theData[count][0],theData[count][1],theData[count][2],theData[count][3])
                        theData.pop(count)
                        print('Interface call!!!!!')
                    elif p.poll() == 2:
                        theProcesses.pop(count)
                        theData.pop(count)
                        print('Network Error')
                    count = count + 1

gotime = initiator()
gotime.initiate()
exit()
