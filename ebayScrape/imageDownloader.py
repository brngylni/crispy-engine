import openpyxl
import requests
import shutil
import time
filename = "scraped/sovereign_pr.xlsx"

book = openpyxl.load_workbook(filename)
sheet = book.active

i = 2
while i < sheet.max_row:
    id = sheet[f"B{i}"].value
    url = sheet[f"D{i}"].value
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        response.raw.decode_content = True
        with open(f"images/sovereign_pr/{id}.jpg", "wb") as file:
            shutil.copyfileobj(response.raw, file)
            print(f"Image {id} has successfuly downloaded")
            i += 1
            time.sleep(1)
    else:
        print("Couldn't connect to url.")
        i += 1
        time.sleep(2)



book.close()

