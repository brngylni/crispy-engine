import os
import smtplib
from email import encoders
from email.message import EmailMessage
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import sqlite3
from datetime import datetime
import imghdr

from PyQt5.QtWidgets import QMessageBox

from GroupsDal import GroupsDal
from MailDal import MailDal
from ProvidersDal import ProvidersDal


class ProductsDal:

    @staticmethod
    def getProducts():
        query = "SELECT * FROM Products"
        connection = sqlite3.connect("barcodeDB.db")
        cursor = connection.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        connection.close()
        return results


    @staticmethod
    def getSku(productId):
        query = "SELECT * FROM Product_Group WHERE (id=%d)" % productId
        connection = sqlite3.connect("barcodeDB.db")
        cursor = connection.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        connection.close()
        return results

    @staticmethod
    def newProduct(barcodeNumber, name, quantity, image1, image2, skus, labels):
        currentDate = str(datetime.now())
        if name is not None or barcodeNumber is not None:
            values = "%s', %d, '%s', 0, 0, '%s','%s','%s', " % (name, quantity, currentDate, barcodeNumber, image1, image2)
            columns = "name', 'quantity', 'dateInward', 'sold', 'saleRate', 'barcodeNumber', 'image1', 'image2', "
            for sku in skus:
                if sku.text() is None or sku.text() == "":
                    values = values + " '',"
                else:
                    values = values + " '%s', " % sku.text()
            values = values[:-2]
            for column in labels:
                if column.text() is None or column.text() == "":
                    columns = columns + " '',"
                else:
                    columns = columns + " '%s', " % column.text()[:-2]
            columns = columns.replace(":", "")
            columns = columns[:-3]
            query = "INSERT INTO Products('%s') VALUES('%s')" % (columns, values[:-1])
            connection = sqlite3.connect("barcodeDB.db")
            cursor = connection.cursor()
            cursor.execute(query)
            connection.commit()
            cursor.close()
            connection.close()
            return True
        else:
            return False

    @staticmethod
    def addColumn(name):
        query = "ALTER TABLE Products ADD COLUMN '%s' TEXT" % name
        connection = sqlite3.connect("barcodeDB.db")
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
        cursor.close()
        connection.close()

    @staticmethod
    def removeColumn(name):
        try:
            query = "ALTER TABLE Products DROP COLUMN '%s' TEXT" % name
            connection = sqlite3.connect("barcodeDB.db")
            cursor = connection.cursor()
            cursor.execute(query)
            connection.commit()
            cursor.close()
            connection.close()
        except Exception as e :
            pass

    @staticmethod
    def searchProduct(barcodeNumber):
        query = "SELECT * FROM Products WHERE (barcodeNumber = '%s')" % barcodeNumber
        connection = sqlite3.connect("barcodeDB.db")
        cursor = connection.cursor()
        cursor.execute(query)
        results = cursor.fetchone()
        cursor.close()
        connection.close()
        return(results)

    @staticmethod
    def updateInward(window, amount, barcodeNumber):
        today = str(datetime.now())
        connection = sqlite3.connect("barcodeDB.db")
        cursor = connection.cursor()
        currentQuantity = ProductsDal.searchProduct(barcodeNumber)[2]
        amount = amount + currentQuantity
        update = "UPDATE Products SET quantity= %d, dateInward = '%s'  WHERE (barcodeNumber ='%s')" % (amount, today, barcodeNumber)
        cursor.execute(update)
        connection.commit()
        cursor.close()
        connection.close()
        QMessageBox.information(window, "OK", "Mail is sending.")
        if currentQuantity == 0:
            ProductsDal.mailSend("backToStock", barcodeNumber)
        return amount

    @staticmethod
    def outward(window, barcodeNumber, amount):
        product = ProductsDal.searchProduct(barcodeNumber)
        products = ProductsDal.getProducts()
        totalSold = 0
        for i in products:
            totalSold = totalSold + int(i[4])
        try:
            currentQuantity = product[2]
            sold = int(product[4])
        except Exception:
            return False
        if currentQuantity < amount:
            return False
        else:
            currentQuantity = currentQuantity - amount
            if currentQuantity == 0:
                QMessageBox.information(window , "Out of Stock","Mail is sending.")
                ProductsDal.mailSend("outOfStock", barcodeNumber)


            try:
                saleRate = (sold+amount) * 100 / (totalSold+amount)
            except Exception:
                saleRate = 0
            time = str(datetime.now())
            statement = "UPDATE Products SET quantity=%d, sold=%d, saleRate=%2f, dateOutward='%s' WHERE (barcodeNumber='%s')" % (currentQuantity, sold+amount, saleRate,time, barcodeNumber)
            connection = sqlite3.connect("barcodeDB.db")
            cursor = connection.cursor()
            cursor.execute(statement)
            connection.commit()
            cursor.close()
            connection.close()
            return True

    @staticmethod
    def edit(barcode, name, dateInward, sold, image1, image2, labels, fields):
        col = ""
        i=0
        for label in labels:
            col = col + f"'{label.text()[:-3]}' = '{fields[i].text()}', "
            i += 1
        values = "name'='%s', 'dateInward' = '%s', 'sold'=%d, 'image1'='%s', 'image2'='%s', '%s'" % (
        name, dateInward, int(sold), image1, image2, col[1:-1])
        statement = "UPDATE Products SET '%s' WHERE barcodeNumber = '%s' " %(values[:-5], barcode)
        connection = sqlite3.connect("barcodeDB.db")
        cursor = connection.cursor()
        cursor.execute(statement)
        connection.commit()
        cursor.close()
        connection.close()

    @staticmethod
    def mailSend(type, barcode):
        product = ProductsDal.searchProduct(barcode)
        groups = GroupsDal.getGroups()
        i = 10
        string = ""
        for group in groups:
            string = f"{string} {group[1]} = {product[i]}, "
            i += 1
        content1 = f"Product with {product[6]} barcode number and '%s' SKU numbers is out of stock." % string[:-2]
        content2 = f"Product with {product[6]} barcode number and '%s' SKU numbers is back to stock" % string[:-2]
        senders = ProvidersDal.getSenders()
        receivers = MailDal.getMails()
        for sender in senders:
            try:
                address = sender[1]
                password = sender[2]
                if sender[3] == "Google":
                    mail = smtplib.SMTP("smtp.gmail.com", 587)
                    mail.ehlo()
                    mail.starttls()
                    mail.login(address, password)
                    for receiver in receivers:
                        if type == "outOfStock":
                            msg = MIMEMultipart()
                            msg['Subject'] = "Product Notification"
                            msg['From'] = address
                            msg['To'] = receiver[1]
                            msg.attach(MIMEText(content1, "plain"))
                            try:
                                image = product[7]
                                with open(image, "rb") as file:
                                    name , type = os.path.splitext(file.name)
                                    type = type.split(".")[1]
                                    msg.attach(MIMEImage(file.read(), type, name=image))
                            except Exception:
                                pass
                            mail.sendmail(address, receiver[1], msg.as_string())
                        else:
                            msg = MIMEMultipart()
                            msg['Subject'] = "Product Notification"
                            msg['From'] = address
                            msg['To'] = receiver[1]
                            msg.attach(MIMEText(content2, "plain"))
                            try:
                                image = product[7]
                                with open(image, "rb") as file:
                                    name, type = os.path.splitext(file.name)
                                    type = type.split(".")[1]
                                    msg.attach(MIMEImage(file.read(), type, name=image))
                            except Exception:
                                pass
                            mail.sendmail(address, receiver[1], msg.as_string())
                    mail.quit()
            except Exception as e:
                continue
