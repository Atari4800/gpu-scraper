import subprocess
import sys
import re
import json

with open("productList.json", "r") as data_file:
    data = json.load(data_file)

with open('defaultBrowser.txt') as fp:
    browser = fp.readline()

for URL in data['Product']:
    URLstr=str(URL['productLink'])
    if re.search("www.bestbuy.com/", URLstr) :
        subprocess.Popen(["python3", "getBB.py", URL['productLink'], browser])
#   if re.search("www.newegg.com/", URLstr) :
#       subprocess.Popen(["python3", "getNE.py", URL['productLink'], browser])
#   if re.search("www.bhphotovideo.com/", URLstr) :
#       subprocess.Popen(["python3", "getBH.py", URL['productLink'], browser])

