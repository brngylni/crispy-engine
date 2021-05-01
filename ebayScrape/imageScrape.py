from selenium import webdriver
import openpyxl, time, shutil, requests, os
from selenium.webdriver.common.keys import Keys


browser = webdriver.Chrome("chromedriver.exe")

file = openpyxl.load_workbook("scraped/sovereign_xf.xlsx")
sheet = file.active

i = 2

while i <= sheet.max_row:
    id = sheet[f"B{i}"].value
    url = f"http://www.ebay.com/itm/{id}"
    filename = f"images/sovereign_xf/{id}.jpg"
    j = 2
    browser.get(url)
    time.sleep(2)
    if "Error" not in browser.title:
        try:
            originalListing = browser.find_element_by_class_name("vi-original-listing")
            originalListing.click()
            time.sleep(2)
            body = browser.find_element_by_class_name("vi-contv2")
            body.send_keys(Keys.SPACE)
            body.send_keys(Keys.SPACE)
            time.sleep(1)
        except Exception as e:
            print("This is already a listing.")
            time.sleep(2)
        finally:
            try:
                mainImg = browser.find_element_by_class_name("fs_imgc")
                images = mainImg.find_elements_by_tag_name("img")
                for image in images:
                    imgUrl = image.get_attribute("src")
                    response = requests.get(imgUrl, stream=True)
                    if response.status_code == 200:
                        response.raw.decode_content = True
                        while os.path.exists(filename):
                            filename = f"images/sovereign_xf/{id}-{j}.jpg"
                            j += 1
                        with open(filename, "wb") as file:
                            shutil.copyfileobj(response.raw, file)
                            print(f"Image {filename} successfuly downloaded.")
                        time.sleep(2)

                    else:
                        print("Unconnected.")
                        time.sleep(2)
            except Exception as e:
                print(e)
                print("This listing has no additional image.")
            finally:
                i += 1
                time.sleep(3)

    else:
        print("Too old listing.")
        i += 1
        time.sleep(3)


browser.close()