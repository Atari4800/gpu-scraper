import subprocess,sys, re

count = 0
file1 = open('URLList.txt')
f2 = open('defaultBrowser.txt') #Refactor to make file (xdg-settings get default-web-browser >> *WHATEVERFILENAME*)
browser = f2.readline()
f2.close()
while True:
    count+=1
    URL = file1.readline()
    if re.search('www.bestbuy.com/',URL):
        subprocess.run(["python3","getBB.py",URL,browser])

    if not URL:
        file1.close()
        break
