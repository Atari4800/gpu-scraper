import initiator
import pytest

test_obj = initiator()

def test_init():
    assert test_obj.prodLink == 'productList.json'
    assert test_obj.defaultBrowser == ''
    assert test_obj.data == None

def test_setDefaultBrowser():
    test_obj.setDefaultBrowser()
    assert test_obj.defaultBrowser == "firefox.desktop"
    
def test_pollSite():
    result = test_obj.pollSite()
    assert result.returncode == 0

def test_initiate():

