import json

import item_base as ib

label = ""
urlBH = 'https://www.bhphotovideo.com/c/product/1566879-REG/arri_l2_0034025_orbiter_manual_yoke_with.html'
urlBB = "https://www.bestbuy.com/site/hyper-hyperdrive-duo-7-port-usb-c-hub-usb-c-docking-station-for-apple-macbook-pro-and-air-gray/6402923.p?skuId=6402923"
dupURL = "https://www.bestbuy.com/site/evga-geforce-rtx-3080-xc3-ultra-gaming-10gb-gddr6-pci-express-4-0-graphics-card/6432400.p?skuId=6432400"
unsupURL = "https://www.google.com/"
unreaDomain = "https://www.012389a98SFAHczaff234.com"

unnadded_item = "https://www.bestbuy.com/site/dyson-purifier-cool-tp07-smart-air-purifier-and-fan-white-silver/6451339.p?skuId=6451339"

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
    assert test_obj.add_item(unnadded_item, "yep it's an item", 99.0, jsonNoWrite) == -5

def test_add_item():
    with open(test_json, 'r') as test_file:
        test_data = json.load(test_file)
        test_file.close()
    test_obj = ib.item_base()

    assert test_obj.add_item(unnadded_item, None, None, json_file=test_json) == 1

    with open(test_json, 'r') as control_file:
        control_data = json.load(control_file)
        control_file.close()
    assert test_data != control_data
    assert len(test_data['Product']) < len(control_data['Product'])


def test_DeleteItem():
    with open(test_json, 'r') as test_file:
        test_data = json.load(test_file)
        test_file.close()
    test_obj = ib.item_base
    assert test_obj.del_item(url=unnadded_item, json_file=test_json) == 1
    with open(test_json, 'r') as control_file:
        control_data = json.load(control_file)
        control_file.close()
    assert test_data != control_data
    assert len(test_data['Product']) > len(control_data['Product'])


# The following functions are helper functions, the test_ prefex was intentionally ommited
def get_json_data(json_file_name='test_productList.json'):
    """Returns the data in the json file with the given file name."""
    with open(json_file_name, 'r') as json_file:
        data = json.load(json_file)
    return data

def verify_test_productList_data(data):
    """Verifies that the input data is the data we would expect the unmodified test_productList.json file to have (correct number of links, correct product links, links in the correct order)"""
    assert len(data['Product']) == 8
    expected_links = get_expected_links()
    for i in range(8):
        assert data['Product'][i]['productLink'] == expected_links[i]

def get_expected_links():
    """Returns a list of the links we would expect the unmodified test_productList.json file to have (These precise 8 links in the proper order)"""
    expected_links = [
            "https://www.bestbuy.com/site/evga-geforce-rtx-3080-xc3-ultra-gaming-10gb-gddr6-pci-express-4-0-graphics-card/6432400.p?skuId=6432400",
            "https://www.bestbuy.com/site/nvidia-geforce-rtx-3090-24gb-gddr6x-pci-express-4-0-graphics-card-titanium-and-black/6429434.p?skuId=6429434",
            "https://www.bestbuy.com/site/nvidia-geforce-rtx-3080-ti-12gb-gddr6x-pci-express-4-0-graphics-card-titanium-and-black/6462956.p?skuId=6462956",
            "https://www.bestbuy.com/site/apple-watch-series-6-gps-44mm-space-gray-aluminum-case-with-black-sport-band-space-gray/6215931.p?skuId=6215931",
            "https://www.newegg.com/zotac-zt-a30810d-10p/p/N82E16814500514?quicklink=true",
            "https://www.newegg.com/p/0F7-00U2-00008",
            "https://www.bhphotovideo.com/c/product/1614301-REG/asus_rog_strix_rtx3080_o10g_white_rog_strix_geforce_rtx.html",
            "https://www.bestbuy.com/site/hyper-hyperdrive-duo-7-port-usb-c-hub-usb-c-docking-station-for-apple-macbook-pro-and-air-gray/6402923.p?skuId=6402923"
            ]
    return expected_links

def write_data_to_json(data, json_file_name):
    """Writes the given data to the json file with the given file name. Useful for restoring modified json files to their original state."""
    with open(json_file_name, 'w') as json_file:
        json_file.seek(0)
        json.dump(data, json_file, indent=4)

# The following are a series of thorough tests to verify that add_item works for various cases
# Each test tries to add a single link. There should be two tests for each supported website: one of which will probably be available and the other probably unavailable
def test_add_item_BB_1():
    """Verifies that the add_item works for this Best Buy link (most likely available product)"""

    # Get the data from test_productList.json and verify it is the correct control data
    control_data = get_json_data()
    verify_test_productList_data(control_data)

    # Attempt to add the new_url to the test_productList.json file
    new_url = 'https://www.bestbuy.com/site/logitech-m510-wireless-laser-mouse-silver-black/9928441.p?skuId=9928441'
    result = ib.item_base.add_item(url=new_url, title=None, price=None, json_file='test_productList.json')
    
    # Verify that the new_url was properly added to the test_productList.json file by verifying the following:
    # -The add_item returned 1 for successful addition,
    # -The test_productList.json file now has 9 products
    # -The test_productList.json contains the links it had before and the new one, all in the proper order
    assert result == 1
    new_data = get_json_data()
    assert len(new_data['Product']) == 9
    expected_links = get_expected_links()
    expected_links.append(new_url)
    for i in range(9):
        assert new_data['Product'][i]['productLink'] == expected_links[i]
    
    # Restore the state of the json file to its original state
    write_data_to_json(control_data, 'test_productList.json')

def test_add_item_BB_2():
    """Verifies that the add_item works for this Best Buy link (most likely unavailable product)"""

    # Get the data from test_productList.json and verify it is the correct control data
    control_data = get_json_data()
    verify_test_productList_data(control_data)

    # Attempt to add the new_url to the test_productList.json file
    new_url = 'https://www.bestbuy.com/site/evga-nvidia-geforce-rtx-3060-xc-gaming-12gb-gddr6-pci-express-4-0-graphics-card/6454329.p?skuId=6454329'
    result = ib.item_base.add_item(url=new_url, title=None, price=None, json_file='test_productList.json')
    
    # Verify that the new_url was properly added to the test_productList.json file by verifying the following:
    # -The add_item returned 1 for successful addition,
    # -The test_productList.json file now has 9 products
    # -The test_productList.json contains the links it had before and the new one, all in the proper order
    assert result == 1
    new_data = get_json_data()
    assert len(new_data['Product']) == 9
    expected_links = get_expected_links()
    expected_links.append(new_url)
    for i in range(9):
        assert new_data['Product'][i]['productLink'] == expected_links[i]
    
    # Restore the state of the json file to its original state
    write_data_to_json(control_data, 'test_productList.json')

def test_add_item_BH_1():
    """Verifies that the add_item works for this B&H link (most likely available product)"""

    # Get the data from test_productList.json and verify it is the correct control data
    control_data = get_json_data()
    verify_test_productList_data(control_data)

    # Attempt to add the new_url to the test_productList.json file
    new_url = 'https://www.bhphotovideo.com/c/product/1576452-REG/crucial_ct16g4sfra32a_16gb_ddr4_3200_mt_s.html' 
    result = ib.item_base.add_item(url=new_url, title=None, price=None, json_file='test_productList.json')
    
    # Verify that the new_url was properly added to the test_productList.json file by verifying the following:
    # -The add_item returned 1 for successful addition,
    # -The test_productList.json file now has 9 products
    # -The test_productList.json contains the links it had before and the new one, all in the proper order
    assert result == 1
    new_data = get_json_data()
    assert len(new_data['Product']) == 9
    expected_links = get_expected_links()
    expected_links.append(new_url)
    for i in range(9):
        assert new_data['Product'][i]['productLink'] == expected_links[i]
    
    # Restore the state of the json file to its original state
    write_data_to_json(control_data, 'test_productList.json')

def test_add_item_BH_2():
    """Verifies that the add_item works for this B&H link (most likely unavailable product)"""

    # Get the data from test_productList.json and verify it is the correct control data
    control_data = get_json_data()
    verify_test_productList_data(control_data)

    # Attempt to add the new_url to the test_productList.json file
    new_url = 'https://www.bhphotovideo.com/c/product/1602756-REG/asus_strixrtx3070o8_rog_strix_geforce_rtx.html' 
    result = ib.item_base.add_item(url=new_url, title=None, price=None, json_file='test_productList.json')
    
    # Verify that the new_url was properly added to the test_productList.json file by verifying the following:
    # -The add_item returned 1 for successful addition,
    # -The test_productList.json file now has 9 products
    # -The test_productList.json contains the links it had before and the new one, all in the proper order
    assert result == 1
    new_data = get_json_data()
    assert len(new_data['Product']) == 9
    expected_links = get_expected_links()
    expected_links.append(new_url)
    for i in range(9):
        assert new_data['Product'][i]['productLink'] == expected_links[i]
    
    # Restore the state of the json file to its original state
    write_data_to_json(control_data, 'test_productList.json')

def test_add_item_NE_1():
    """Verifies that the add_item works for this Newegg link (most likely available product)"""

    # Get the data from test_productList.json and verify it is the correct control data
    control_data = get_json_data()
    verify_test_productList_data(control_data)

    # Attempt to add the new_url to the test_productList.json file
    new_url = 'https://www.newegg.com/msi-geforce-gtx-1660-super-gtx-1660-super-ventus-xs-oc/p/N82E16814137475' 
    result = ib.item_base.add_item(url=new_url, title=None, price=None, json_file='test_productList.json')
    
    # Verify that the new_url was properly added to the test_productList.json file by verifying the following:
    # -The add_item returned 1 for successful addition,
    # -The test_productList.json file now has 9 products
    # -The test_productList.json contains the links it had before and the new one, all in the proper order
    assert result == 1
    new_data = get_json_data()
    assert len(new_data['Product']) == 9
    expected_links = get_expected_links()
    expected_links.append(new_url)
    for i in range(9):
        assert new_data['Product'][i]['productLink'] == expected_links[i]
    
    # Restore the state of the json file to its original state
    write_data_to_json(control_data, 'test_productList.json')

def test_add_item_NE_2():
    """Verifies that the add_item works for this Newegg link (most likely unavailable product)"""

    # Get the data from test_productList.json and verify it is the correct control data
    control_data = get_json_data()
    verify_test_productList_data(control_data)

    # Attempt to add the new_url to the test_productList.json file
    new_url = 'https://www.newegg.com/asus-geforce-rtx-3080-ti-tuf-rtx3080ti-12g-gaming/p/N82E16814126510?Item=N82E16814126510'
    result = ib.item_base.add_item(url=new_url, title=None, price=None, json_file='test_productList.json')
    
    # Verify that the new_url was properly added to the test_productList.json file by verifying the following:
    # -The add_item returned 1 for successful addition,
    # -The test_productList.json file now has 9 products
    # -The test_productList.json contains the links it had before and the new one, all in the proper order
    assert result == -6
    new_data = get_json_data()
    assert len(new_data['Product']) == 8
    expected_links = get_expected_links()
    for i in range(8):
        assert new_data['Product'][i]['productLink'] == expected_links[i]
    
    # Restore the state of the json file to its original state
    write_data_to_json(control_data, 'test_productList.json')
