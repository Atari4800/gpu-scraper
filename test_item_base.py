import json

import pytest
import item_base as ib

label = ""
urlBH = 'https://www.bhphotovideo.com/c/product/1566879-REG/arri_l2_0034025_orbiter_manual_yoke_with.html'
urlBB = "https://www.bestbuy.com/site/hyper-hyperdrive-duo-7-port-usb-c-hub-usb-c-docking-station-for-apple-macbook-pro-and-air-gray/6402923.p?skuId=6402923"
dupURL = "https://www.bestbuy.com/site/evga-geforce-rtx-3080-xc3-ultra-gaming-10gb-gddr6-pci-express-4-0-graphics-card/6432400.p?skuId=6432400"
unsupURL = "https://www.google.com/"
unreaDomain = "https://www.012389a98SFAHczaff234.com"

itemNotFound = "https://www.bestbuy.com/"
jsonNoWrite = "test_productListNoWrite.json"
problemJSON = 'test_json_can\'tread.json'
control_json = 'control_productList.json'
test_json = 'test_productList.json'

def test_addDuplicateItem():
    test_obj = ib.item_base()
    assert test_obj.add_item(dupURL, None, None, test_json) == -5

def test_addUnsupported():
    test_obj = ib.item_base()
    assert test_obj.add_item(unsupURL, None, None, test_json) == -4

def test_addUnreachableDomain():
    test_obj = ib.item_base()
    assert test_obj.add_item(unreaDomain, None, None, test_json) == -3

def test_addBadJSON():
    test_obj = ib.item_base()
    assert test_obj.add_item(urlBB, None, None, problemJSON) == -2

def test_additemNotFound():
    test_obj = ib.item_base()
    assert test_obj.add_item(itemNotFound, None, None, test_json) == -1

def test_addJSONWriteError():
    test_obj = ib.item_base()
    assert test_obj.add_item(urlBB, None, None, jsonNoWrite) == 0

def test_add_itemBB():
    test_obj = ib.item_base()
    assert test_obj.add_item(urlBB, None, None, json_file=test_json)
    with open(test_json, 'r') as test_file:
        test_data = json.load(test_file)
        with open(control_json, 'r') as control_file:
            control_data = json.load(control_file)
            assert test_data == control_data
"""
def test_DeleteItemBH():
    test_obj = ib.item_base()
    assert test_obj.delItem(urlBH, json_file=test_json) == 1
    with open(test_json, 'r') as test_file:
        test_data = json.load(test_file)
        with open(control_json, 'r') as control_file:
            control_data = json.load(control_file)
            assert test_data == control_data
        with open(control_json, 'r') as control_data:
            test_obj.delItem(urlBB, json_file=test_json)
            assert test_data != control_data



def test_delItem():
    test_obj = ib.item_base
    test_obj.delItem(url, json_file=control_json)
    test_obj.delItem(url, json_file=test_json)
    with open(test_json, 'r') as test_file:
        with open(control_json, 'r') as control_file:
            assert test_file == control_file
    test_obj.add_item(url,json_file=control_file)
"""
