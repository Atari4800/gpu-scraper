import scraper as sc


good_stock_urlBB = 'https://www.bestbuy.com/site/apple-watch-series-6-gps-44mm-space-gray-aluminum-case-with-black-sport-band-space-gray/6215931.p?skuId=6215931'

bad_stock_urlBB = 'https://www.bestbuy.com/site/nvidia-geforce-rtx-3080-ti-12gb-gddr6x-pci-express-4-0-graphics-card-titanium-and-black/6462956.p?skuId=6462956'

good_stock_BH = "https://www.bhphotovideo.com/c/product/1383479-REG/godox_ad600pro_witstro_all_in_one_outdoor.html"
bad_stock_BH = "https://www.bhphotovideo.com/c/product/1614301-REG/asus_rog_strix_rtx3080_o10g_white_rog_strix_geforce_rtx.html?sts=pi&pim=Y"

good_stock_NE = "https://www.newegg.com/acer-c740-c4pe/p/2S3-0008-003F8"
bad_stock_NE = "https://www.newegg.com/evga-geforce-rtx-3080-10g-p5-3897-kr/p/N82E16814487518?Item=N82E16814487518"
invalid_url = 'blah'

def test_init_valid():
    test_obj = sc.scraper(URL=good_stock_urlBB, uType="BB")
    assert test_obj.URL == good_stock_urlBB

def test_init_invalid(): 
    test_obj = sc.scraper(URL=good_stock_urlBB, uType=None)
    assert test_obj.uType == None

def test_getBB_good():
    test_obj = sc.scraper(URL=good_stock_urlBB, uType="BB")
    assert test_obj.getBB() == 1

def test_getBB_bad():
    test_obj = sc.scraper(URL=bad_stock_urlBB, uType="BB")
    assert test_obj.getBB() == 0

def test_getBH_good():
    test_obj = sc.scraper(URL=good_stock_BH, uType="BH")
    assert test_obj.getBH() == 1

def test_getBH_Bad():
    test_obj = sc.scraper(URL=bad_stock_BH, uType="BH")
    assert test_obj.getBH() == 0

def test_getNE_Good():
    test_obj = sc.scraper(URL=good_stock_NE, uType="BH")
    assert test_obj.getNE() == 1

def test_getNE_Bad():
    test_obj = sc.scraper(URL=bad_stock_NE, uType="BH")
    assert test_obj.getNE() == 0
