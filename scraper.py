import subprocess,sys, re

count = 0
file1 = open('URLList.txt')
while True:
    count+=1
    URL = file1.readline()
    if re.search('www.bestbuy.com/',URL):
        subprocess.run(["python3","getBB.py",URL])

    if not URL:
        file1.close()
        break
