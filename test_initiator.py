import json

import initiator as it
import pytest



def test_init():
    test_obj = it.Initiator(the_products="control_productList.json")
    assert test_obj.prod_link == 'control_productList.json'
    assert test_obj.default_browser == 'firefox.desktop'
    assert test_obj.data == None

def test_setDefaultBrowser():
    test_obj = it.Initiator(the_products="control_productList.json")
    test_obj.set_default_browser()
    assert test_obj.default_browser == "firefox.desktop"

def test_pollSiteIP():
    test_obj = it.Initiator(the_products="control_productList.json")
    assert test_obj.poll_site("8.8.8.8") == True
def test_pollSitePartialURL():
    test_obj = it.Initiator(the_products="control_productList.json")
    assert test_obj.poll_site("www.google.com") == True
def test_pollSiteFullURL():
    test_obj = it.Initiator(the_products="control_productList.json")
    assert test_obj.poll_site("https://www.google.com/") == True
def test_pollSiteBadURL():
    test_obj = it.Initiator(the_products="control_productList.json")
    assert test_obj.poll_site("https://www.23971gsadbhefasdWQ@.com/") == False
def test_pollSiteEmpty():
    test_obj = it.Initiator(the_products="control_productList.json")
    assert test_obj.poll_site("") == False
def test_initiateNoJSON():
    test_obj = it.Initiator(the_products="")
    assert test_obj.initiate() == 0
def test_initiateMalformedJSON():
    test_obj = it.Initiator(the_products="control_productList.js")
    assert test_obj.initiate() == 0
def test_initiateWrongJSONFile():
    test_obj = it.Initiator(the_products="control_bad_productList.js")
    assert test_obj.initiate() == 0
def test_initiateEmptyJSON():
    test_obj = it.Initiator(the_products="control_bad_productList.js")
    assert test_obj.initiate() == 0
def test_initiateProductsExist():
    test_obj = it.Initiator(the_products="control_productList.json")
    with open("control_productList.json", "r") as data_file:
        data = json.load(data_file)
    assert test_obj.initiate() == len(data['Product'])



