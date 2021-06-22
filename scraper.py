import subprocess,sys, re,json

with open("productList.json","r") as read_file:
    data = json.load(read_file)
count = 0
file1 = open('URLList.txt')
f2 = open('defaultBrowser.txt') #Refactor to make file (xdg-settings get default-web-browser >> *WHATEVERFILENAME*)
browser = f2.readline()
f2.close()
for URL in data['Product']:
    print(URL)
    subprocess.Popen(["python3","getBB.py",URL['productLink'],browser])
