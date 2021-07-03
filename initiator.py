import subprocess
import sys
import re
import json

with open("productList.json", "r") as data_file:
    data = json.load(data_file)

with open('defaultBrowser.txt') as fp:
    browser = fp.readline()
theProcesses=[]
for URL in data['Product']:

    URLstr=str(URL['productLink'])
    print('running for ' + URLstr)
    if re.search("www.bestbuy.com/", URLstr) :
        theProcesses.append(subprocess.Popen(["python3", "scraper.py", URL['productLink'], 'BB', browser]))
    if re.search("www.newegg.com/", URLstr) :
        theProcesses.append(subprocess.Popen(["python3", "scraper.py", URL['productLink'], 'NE', browser]))
    if re.search("www.bhphotovideo.com/", URLstr) :
        theProcesses.append(subprocess.Popen(["python3", "scraper.py", URL['productLink'], 'BH', browser]))

    while len(theProcesses) > 3:
        for p in theProcesses :
            if p.poll() == 0:
                theProcesses.remove(p)
            elif p.poll() == 1:
                theProcesses.remove(p)
                print('Interface call!!!!!')
            elif p.poll() == 2:
                print('Network Error')


exit()
