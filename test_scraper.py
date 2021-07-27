import scraper as sc

good_stock_urlBB = 'https://www.bestbuy.com/site/apple-watch-series-6-gps-44mm-space-gray-aluminum-case-with-black' \
                   '-sport-band-space-gray/6215931.p?skuId=6215931 '

bad_stock_urlBB = 'https://www.bestbuy.com/site/nvidia-geforce-rtx-3080-ti-12gb-gddr6x-pci-express-4-0-graphics-card' \
                  '-titanium-and-black/6462956.p?skuId=6462956 '

good_stock_BH = "https://www.bhphotovideo.com/c/product/1383479-REG/godox_ad600pro_witstro_all_in_one_outdoor.html"
bad_stock_BH = "https://www.bhphotovideo.com/c/product/1614301-REG" \
               "/asus_rog_strix_rtx3080_o10g_white_rog_strix_geforce_rtx.html?sts=pi&pim=Y "

good_stock_NE = "https://www.newegg.com/acer-c740-c4pe/p/2S3-0008-003F8"
bad_stock_NE = "https://www.newegg.com/evga-geforce-rtx-3080-10g-p5-3897-kr/p/N82E16814487518?Item=N82E16814487518"
invalid_url = 'blah'

def test_get_fields_bb():
    test_fields = ['Apple Watch Series 6 (GPS) 44mm Space Gray Aluminum Case with Black Sport Band - Space Gray', 429.0]
    assert sc.Scraper.get_fields_bb(good_stock_urlBB, None, None) == test_fields

def test_get_fields_ne():
    test_fields = ['Acer C740-C4PE 11.6" Chromebook Intel Celeron 3205u X2 1.5GHz 4GB memory, 16GB SSD, Intel HD Graphics, Chrome OS - NX.EF2AA.002 - C-Grade', 59.99]
    assert sc.Scraper.get_fields_ne(good_stock_NE, None, None) == test_fields

def test_get_fields_bh():
    test_fields = ['Godox AD600Pro Witstro All-in-One Outdoor Flash', 899.0]
    assert sc.Scraper.get_fields_bh(good_stock_BH, None, None) == test_fields

def test_get_fields_bb_bad_url():
    assert sc.Scraper.get_fields_bb("www.google.com", None, None) == [None,None]

def test_get_fields_ne_bad_url():
    assert sc.Scraper.get_fields_ne("http://www.google.com", None, None) == [None,None]
def test_get_fields_bh_bad_url():
    assert sc.Scraper.get_fields_bh("https://www.google.com", None, None) == [None,None]

def test_init_valid():
    test_obj = sc.Scraper(url=good_stock_urlBB, url_type="BB")
    assert test_obj.url == good_stock_urlBB

def test_init_invalid():
    test_obj = sc.Scraper(url=good_stock_urlBB, url_type=None)
    assert test_obj.store_type is None


def test_get_bb_good():
    test_obj = sc.Scraper(url=good_stock_urlBB, url_type="BB")
    assert test_obj.get_bb() == 1


def test_get_bb_bad():
    test_obj = sc.Scraper(url=bad_stock_urlBB, url_type="BB")
    assert test_obj.get_bb() == 0


def test_get_bh_good():
    test_obj = sc.Scraper(url=good_stock_BH, url_type="BH")
    assert test_obj.get_bh() == 1


def test_get_bh_bad():
    test_obj = sc.Scraper(url=bad_stock_BH, url_type="BH")
    assert test_obj.get_bh() == 0


def test_get_ne_good():
    test_obj = sc.Scraper(url=good_stock_NE, url_type="NE")
    assert test_obj.get_ne() == 1


def test_get_ne_bad():
    test_obj = sc.Scraper(url=bad_stock_NE, url_type="NE")
    assert test_obj.get_ne() == 0
