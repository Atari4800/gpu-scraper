from interface import shorten_url

def test_shorten_url_common_input():
    assert shorten_url("https://www.bestbuy.com/site/evga-geforce-rtx-3080-xc3-ultra-gaming-10gb-gddr6-pci-express-4-0-graphics-card/6432400.p?skuId=6432400") == "Best Buy"
    assert shorten_url("https://www.bestbuy.com/site/nvidia-geforce-rtx-3090-24gb-gddr6x-pci-express-4-0-graphics-card-titanium-and-black/6429434.p?skuId=6429434") == "Best Buy"
    
    assert shorten_url("https://www.newegg.com/zotac-zt-a30810d-10p/p/N82E16814500514?quicklink=true") == "Newegg"
    assert shorten_url("https://www.newegg.com/p/0F7-00U2-00008") == "Newegg"

    assert shorten_url("https://www.bhphotovideo.com/c/product/1614301-REG/asus_rog_strix_rtx3080_o10g_white_rog_strix_geforce_rtx.html") == "B&H"
    assert shorten_url("https://www.bhphotovideo.com/c/product/1566879-REG/arri_l2_0034025_orbiter_manual_yoke_with.html") == "B&H"

def test_shorten_url_other():
    assert shorten_url("https://realpython.com/pytest-python-testing/") == "Other"
    assert shorten_url("https://www.unr.edu/cse/undergraduates/prospective-students/what-is-software-engineering") == "Other"
    assert shorten_url("") == "Other"
    assert shorten_url("  ") == "Other"
    assert shorten_url("asdf") == "Other"
