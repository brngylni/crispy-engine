import pandas as pd

excelFile = pd.read_excel("scraped/sovereign_xf.xlsx", sheet_name="sovereign")

jsonFile  =  excelFile.to_json(r"scraped/sovereign_xf.json" ,orient = "records")





