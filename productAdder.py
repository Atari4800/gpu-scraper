import json, sys, re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options as FFOpt
from bs4 import BeautifulSoup





with open("productList.json.save", "r") as dataFile:
    data = json.load(dataFile)
type = sys.argv[1]
URL = sys.argv[2]

for URLStr in data['Product'] :
    if str(URLStr['productLink']) == URL :
        print("Duplicate URL, cannot add.")
        exit(1)
print("Adding URL...")

theDriver = './drivers/geckodriver'
option = FFOpt()
option.headless = True
browser = webdriver.Firefox(options = option, executable_path = theDriver)
browser.get(URL)
title = ' '
price = ' '
soup = BeautifulSoup(browser.page_source,'html.parser')

if re.search("www.bestbuy.com/", URL) :
    results = soup.find(class_ = 'sku-title')
    results = results.find(class_ = 'heading-5 v-fw-regular')
    title=str(results)[len('h1 class = \"heading-5 v-fw-regular\"'):-len('</h1>')]
    print('Item is called ' +title)
    results = soup.find(class_ = 'priceView-hero-price priceView-customer-price')
    print(results)
    priceStr=str(results)
    price=float(priceStr[priceStr.index('aria-hidden="true">') + len('aria-hidden="true">') +1:priceStr.index('</span><span class')])
    print('The price is ' + str(price))
elif re.search("www.newegg.com/",URL) :
    results = soup.find(class_ = 'product-title')
    title = str(results)[len('<h1 class=\"product-title\">'):-len('</h1>')]
    print(title)
    results = soup.find(class_ = 'product-price')
    priceStr=results.get_text()
    if re.search('Sale',priceStr) :
        price = re.findall("\d+\.\d+",priceStr)
        price = float(price[0])
        print(str(price))
    else:
        price=float(priceStr.split('$')[1].replace(',',''))
elif re.search("www.bhphotovideo.com",URL) :
    results = soup.find(class_ = 'title_1S1JLm7P93Ohi6H_hq7wWh')
    if results == None :
        print('B&H bot detection has picked you up. Please increase product checking interval in the scheduler. Then go to B&H\'s website to do their recaptcha and try again.')
        browser.close()
        exit()
    title=results.get_text().split('BH')[0]
    print(title)
    results = soup.find(class_ = 'price_1DPoToKrLP8uWvruGqgtaY')
    priceStr=results.get_text()
    price = float(priceStr.split('$')[1].replace(',',''))
    print(price)
else:
    print("The text which was input is not supported")
    browser.close()
    exit()

browser.close()



print("URL Added Successfully.")

jsonObj = {'productType':title,'productLink':URL,'productPrice':price}
data['Product'].append(jsonObj)
dataFile = open('productList.json','w+')
dataFile.seek(0)

json.dump(data,dataFile)
dataFile.truncate()
dataFile.close()
