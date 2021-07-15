from interface import shortenURL

def test_shortenURL_common_input():
    assert shortenURL("https://www.bestbuy.com/site/evga-geforce-rtx-3080-xc3-ultra-gaming-10gb-gddr6-pci-express-4-0-graphics-card/6432400.p?skuId=6432400") == "Best Buy"
    assert shortenURL("https://www.bestbuy.com/site/nvidia-geforce-rtx-3090-24gb-gddr6x-pci-express-4-0-graphics-card-titanium-and-black/6429434.p?skuId=6429434") == "Best Buy"
    
    assert shortenURL("https://www.newegg.com/zotac-zt-a30810d-10p/p/N82E16814500514?quicklink=true") == "Newegg"
    assert shortenURL("https://www.newegg.com/p/0F7-00U2-00008") == "Newegg"

    assert shortenURL("https://www.bhphotovideo.com/c/product/1614301-REG/asus_rog_strix_rtx3080_o10g_white_rog_strix_geforce_rtx.html") == "B&H"
    assert shortenURL("https://www.bhphotovideo.com/c/product/1566879-REG/arri_l2_0034025_orbiter_manual_yoke_with.html") == "B&H"

def test_shortenURL_valid_URL():
    assert shortenURL("https://realpython.com/pytest-python-testing/") == "realpython.com"
    assert shortenURL("https://www.youtube.com/watch?v=wqaFYeZ6D3o") == "www.youtube.com"
    assert shortenURL("https://www.tutorialspoint.com/pytest/index.htm") == "www.tutorialspoint.com"
    assert shortenURL("https://pypi.org/project/pytest/") == "pypi.org"
    assert shortenURL("https://www.unr.edu/cse/undergraduates/prospective-students/what-is-software-engineering") == "www.unr.edu"

def test_shortenURL_invalid_URL():
    assert shortenURL("") == ""
    assert shortenURL("  ") == "  "
    assert shortenURL("htp://www.youtube.com/asdf") == "htp://www.youtube.com/asdf"
    assert shortenURL("https//www.youtube.com/asdf") == "https//www.youtube.com/asdf"
    assert shortenURL("asdf://www.youtube.com/asdf") == "asdf://www.youtube.com/asdf"
    assert shortenURL("https:/www.youtube.com/asdf") == "https:/www.youtube.com/asdf"
    assert shortenURL("asdfasdf") == "asdfasdf"
    assert shortenURL("https://www.youtube/asdf") == "https://www.youtube/asdf"
    assert shortenURL("https://www.youtube.moc/asdf") == "https://www.youtube.moc/asdf"
