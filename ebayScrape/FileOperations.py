import openpyxl


class FileOperations:
    __book = openpyxl.load_workbook("scraped/sovereign_pr.xlsx")
    __sheet = __book.active

    @staticmethod
    def writer(listings):
        row = FileOperations.__sheet.max_row + 1
        for i in listings:
            FileOperations.__sheet[f"A{row}"] = i[0]
            FileOperations.__sheet[f"B{row}"] = i[1]
            FileOperations.__sheet[f"C{row}"] = i[2]
            FileOperations.__sheet[f"D{row}"] = i[3]
            FileOperations.__sheet[f"E{row}"] = i[4]
            row += 1
        FileOperations.__book.save("scraped/sovereign_pr.xlsx")

    @staticmethod
    def saveExit():
        FileOperations.__book.save("scraped/sovereign_pr.xlsx")
        FileOperations.__book.close()
