import requests
import unicodedata
from bs4 import BeautifulSoup
import time
import csv


def scrape(className, soup: BeautifulSoup, element):
    if len(soup.find_all("div", class_="match-height")) == 0:
        items = soup.find_all(element, class_=className)
        for item in items:
            itemPage = requests.get(item["href"])
            time.sleep(2)
            itemSoup = BeautifulSoup(itemPage.content, "html.parser")
            scrape(className, itemSoup, element)
    else:
        itemSoup = soup
        containers = itemSoup.find_all("div", class_="match-height")
        for container in containers:
            product = container.find("a")
            productPage = requests.get(product["href"])
            time.sleep(2)
            productSoup = BeautifulSoup(productPage.content, "html.parser")
            productName = productSoup.find("div", class_="box-product-desktop").find("h1").text
            productDescription = productSoup.find("div", class_="box-product-body-inside").text
            productDescription = productDescription[
                                 len(productSoup.find("div", class_="box-product-desktop").text):]
            productDescription = productDescription.replace("\n", "")
            productDescription = productDescription.replace("\r", "")
            productSku = productSoup.find("div", class_="box-product-desktop").find("em").text
            if productSoup.find("p", class_="old-price") is None:
                try:
                    productRegularPrice = productSoup.find("span", class_="price-including-tax").find("span",
                                                                                                class_="price").text
                except:
                    productRegularPrice = "No Price"
                finally:
                    productSalePrice = "No Sale"
            else:
                try:
                    productRegularPrice = productSoup.find("p", class_="old-price").find("span", class_="price").text
                    productSalePrice = productSoup.find("span", class_="price-including-tax").find("span",
                                                                                               class_="price").text
                except:
                    productRegularPrice = "No price"
                    productSalePrice = "No Price"
            productRegularPrice.replace("\n", "")
            productSalePrice.replace("\n", "")
            if "(" in productRegularPrice:
                productRegularPrice = productRegularPrice.split("(")[1]
                productRegularPrice = productRegularPrice.split(")")[0]
            productData = [productName, productDescription, productSku, productRegularPrice, productSalePrice]
            images = productSoup.find_all("img", class_="draggable-zoom")
            for image in images:
                productData.append(image["data-src"])
            print(productData)
            try:
                writer.writerow(productData)
            except:
                i = 0
                for data in productData:
                    data = unicodedata.normalize("NFKC", data)
                    productData[i] = data
                    i += 1
                writer.writerow(productData)
        pagination = itemSoup.find("ul", class_="pagination")
        if pagination != None:
            for link in pagination.find_all("a"):
                if link.has_attr("aria-label"):
                    if link["aria-label"] == "Next" and not link.has_attr("disabled"):
                        nextPage = requests.get(link["href"])
                        time.sleep(2)
                        nextPageSoup = BeautifulSoup(nextPage.content, "html.parser")
                        scrape(className, nextPageSoup, element)


file = open("products.csv", "a")
writer = csv.writer(file, delimiter=",", quotechar='"', quoting=csv.QUOTE_ALL)
fields = ["Product Name", "Product Description", "SKU", "Regular Price", "Sale Price", "Images"]
page = requests.get("http://www.website.com")
time.sleep(2)
soup = BeautifulSoup(page.content, "html.parser")
headerMenu = soup.find(class_="box-header-menu-inner")
buttons = headerMenu.find_all("button")

i = 8
while i < len(buttons):
    page = requests.get(buttons[i]["data-link"])
    time.sleep(2)
    soup = BeautifulSoup(page.content, "html.parser")
    scrape("box-listing-item", soup, "a")
    print("scraped")
    i += 1

page = requests.get("other_part_of_website.com")
time.sleep(2)
soup = BeautifulSoup(page.content, "html.parser")
scrape("box-listing-item", soup, "a")

page = requests.get("other_part_of_website.com")
time.sleep(2)
soup = BeautifulSoup(page.content, "html.parser")
scrape("box-listing-item", soup, "a")

page = requests.get("other_part_of_website.com")
time.sleep(2)
soup = BeautifulSoup(page.content, "html.parser")
scrape("box-listing-item", soup, "a")
