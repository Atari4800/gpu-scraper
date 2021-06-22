import os, re

count = 0
file1 = open('URLList.txt')
while True:
	count+=1
	URL = file1.readline()
	if re.search('www.amd.com/',URL):
		os.spawnl(os.P_DETACH,'python3 GetAMD.py')
	if re.search('www.bestbuy.com/',URL):
		os.spawnl(os.P_DETACH,'python3 getBB.py')
	if re.search('www.newegg.com/',URL):
		os.spawnl(os.P_DETACH,'python3 getNE.py')



	if not URL:
		file1.close()
		break
