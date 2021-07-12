import pytest
import scraper


good_stock_url = 'https://www.bestbuy.com/site/apple-watch-series-6-gps-44mm-space-gray-aluminum-case-with-black-sport-band-space-gray/6215931.p?skuId=6215931'

bad_stock_url = 'https://www.bestbuy.com/site/nvidia-geforce-rtx-3080-ti-12gb-gddr6x-pci-express-4-0-graphics-card-titanium-and-black/6462956.p?skuId=6462956'

invalid_url = 'blah'

def test_init_valid():
    test_obj = scraper(good_stock_url, "BB")
    # assert test_ob == something good?

def test_init_invalid(): 
    test_obj = scraper(good_stock_url, None)
    # assert test_obj == None

def test_getBB_good():
    test_obj = scraper(good_stock_url, "BB")
    result = test_obj.getBB()
    assert result == True

def test_getBB_bad 
    test_obj = scraper(bad_stock_url, "BB")
    result = test_obj.getBB()
    assert result == False

def test_getBB_invalid():
    test_obj = scraper(bad_stock_url, "BB")
    result = test_obj.getBB()
    assert result == False

# TODO: Parametrize get__() methods to call different functions with differing urls.
