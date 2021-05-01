from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
from selenium.webdriver.common.keys import Keys
import pickle


class TeraPeak:
    __browser = webdriver.Chrome("chromedriver.exe")
    __url = "http://www.ebay.com"
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def login(self):
        self.__browser.get(self.__url)
        time.sleep(2)
        btnSignIn = self.__browser.find_element_by_id("gh-ug").find_element_by_tag_name("a")
        btnSignIn.click()
        time.sleep(2)
        userInput = self.__browser.find_element_by_id("userid")
        userInput.send_keys(self.username)
        time.sleep(2)
        btnContinue = self.__browser.find_element_by_id("signin-continue-btn")
        btnContinue.click()
        time.sleep(2)
        passInput = self.__browser.find_element_by_id("pass")
        passInput.send_keys(self.password)
        time.sleep(2)
        btnLogin = self.__browser.find_element_by_id("sgnBt")
        btnLogin.click()
        time.sleep(2)

    def goTerapeak(self):
        sellerHub = "http://www.ebay.com/sh"
        time.sleep(2)
        self.__browser.get(sellerHub)
        btnResearch = self.__browser.find_element_by_xpath('//*[@id="s0-0-4-5-36-2[6]-0"]')
        btnResearch.click()
        time.sleep(2)

    def search(self, keyword):
        time.sleep(1)
        keywordField = self.__browser.find_element_by_name("keywords")
        keywordField.send_keys(keyword)
        time.sleep(2)
        siteSelect = self.__browser.find_element_by_class_name("marketplace-select").find_element_by_css_selector("select")
        siteSelect.click()
        time.sleep(2)
        for i in range(0, 21):
            siteSelect.send_keys(Keys.DOWN)
            time.sleep(1)
        siteSelect.send_keys(Keys.ENTER)
        time.sleep(2)
        dataRangeSelect = self.__browser.find_element_by_class_name("data-range-select").find_element_by_css_selector("select")
        dataRangeSelect.click()
        time.sleep(2)
        for i in range(0, 3):
            dataRangeSelect.send_keys(Keys.DOWN)
            time.sleep(1)
        dataRangeSelect.send_keys(Keys.UP)
        time.sleep(2)
        dataRangeSelect.send_keys(Keys.ENTER)
        time.sleep(2)
        btnSearch = self.__browser.find_element_by_class_name("search-button")
        btnSearch.click()
        time.sleep(5)
        btnSearch.click()

    def scrape(self):
        action = ActionChains(self.__browser)
        for i in range(0,5):
            action.send_keys(Keys.SPACE).perform()
            time.sleep(2)

        listingsTable = self.__browser.find_element_by_class_name("grid")
        listingRows = listingsTable.find_elements_by_css_selector("tr")
        i=1

        listingList = []
        while i < len(listingRows):
            try:
                date = listingRows[i].find_element_by_class_name("datelastsold").text
                listingText = listingRows[i].find_element_by_class_name("listing-text")
                idDiv = listingText.find_element_by_css_selector("div")
                itemId = idDiv.get_attribute("data-item-id")
                title = idDiv.text
                imgUrl = listingRows[i].find_element_by_class_name("shui-image-container").find_element_by_tag_name("img").get_attribute("src")
                price = listingRows[i].find_element_by_class_name("avgsalesprice").find_element_by_tag_name("div").text
                individual = [date, itemId, title, imgUrl, price]
                print(individual)
                listingList.append(individual)
            except Exception as e:
                print(e)
            finally:
                i += 1
                time.sleep(2)
        return listingList

    def changePage(self):
        btnNext = self.__browser.find_element_by_class_name("pagination__next")
        btnNext.click()
        time.sleep(5)

    def isNextAble(self):
        btnNext = self.__browser.find_element_by_class_name("pagination__next")
        if btnNext.get_attribute("disabled") == "true":
            return False
        else:
            return True

    def closeBrowser(self):
        self.__browser.close()

    def getCookie(self):
        pickle.dump(self.__browser.get_cookies(), open("cookies.pkl", "wb"))

    def addCookie(self):
        cookies = pickle.load(open("cookies.pkl", "rb"))
        for cookie in cookies:
            self.__browser.add_cookie(cookie)






