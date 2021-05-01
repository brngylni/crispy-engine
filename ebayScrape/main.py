from TeraPeak import TeraPeak
from FileOperations import  *

def initialize(username, password):
    global ebay
    ebay = TeraPeak(username, password)
    try:
        ebay.addCookie()
    except Exception as e :
        print(e)
    ebay.login()
    ebay.goTerapeak()

def scrape(keyword):
    ebay.search(keyword)
    while True:
        if ebay.isNextAble():
            try:
                listings = ebay.scrape()
                FileOperations.writer(listings)
                ebay.changePage()
            except Exception as e:
                print(e)
        else:
            try:
                listings = ebay.scrape()
                FileOperations.writer(listings)
            except Exception as e:
                print(e)
            break

def finalization():
    ebay.getCookie()
    ebay.closeBrowser()
    FileOperations.saveExit()



username = "barankara_2000@hotmail.com"
password = "1598742369bB"
keyword = "sovereign pr"

initialize(username, password)
scrape(keyword)
finalization()