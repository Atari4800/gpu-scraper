import initiator as it
import pytest



def test_init():
    test_obj = it.initiator(theProducts="control_productList.json")
    assert test_obj.prodLink == 'control_productList.json'
    assert test_obj.defaultBrowser == 'firefox.desktop'
    assert test_obj.data == None

def test_setDefaultBrowser():
    test_obj = it.initiator(theProducts="control_productList.json")
    test_obj.setDefaultBrowser()
    assert test_obj.defaultBrowser == "firefox.desktop"

def test_pollSiteIP():
    test_obj = it.initiator(theProducts="control_productList.json")
    assert test_obj.pollSite("8.8.8.8") == True
def test_pollSitePartialURL():
    test_obj = it.initiator(theProducts="control_productList.json")
    assert test_obj.pollSite("www.google.com") == True
def test_pollSiteFullURL():
    test_obj = it.initiator(theProducts="control_productList.json")
    assert test_obj.pollSite("https://www.google.com/") == True
def test_pollSiteBadURL():
    test_obj = it.initiator(theProducts="control_productList.json")
    assert test_obj.pollSite("https://www.23971gsadbhefasdWQ@.com/") == False
def test_pollSiteEmpty():
    test_obj = it.initiator(theProducts="control_productList.json")
    assert test_obj.pollSite("") == False
def test_initiateNoJSON():
    test_obj = it.initiator(theProducts="")
    assert test_obj.initiate() == 0
def test_initiateMalformedJSON():
    test_obj = it.initiator(theProducts="control_productList.js")
    assert test_obj.initiate()==0
def test_initiateWrongJSONFile():
    test_obj = it.initiator(theProducts="control_bad_productList.js")
    assert test_obj.initiate()==0
def test_initiateEmptyJSON():
    test_obj = it.initiator(theProducts="control_bad_productList.js")
    assert test_obj.initiate()==0
def test_initiateProductsExist():
    test_obj = it.initiator(theProducts="control_productList.json")
    assert test_obj.initiate()== 8



