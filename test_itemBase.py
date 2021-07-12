import pytest
import itemBase as ib

label = ""
url = 'https://www.bhphotovideo.com/c/product/1566879-REG/arri_l2_0034025_orbiter_manual_yoke_with.html'

control_json = 'control_productList.json'
test_json = 'test_productList.json'

with open(test_json, 'r') as test_file:
    with open(control_json, 'r') as control_file:
        def test_addItem():
            ib().addItem(url, test_json)
            assert test_file == control_file

        def test_delItem():
            tb().delItem(url, control_json)
            tb().delItem(url, test_json) 
            assert test_file == control_file
