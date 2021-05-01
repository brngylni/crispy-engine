import sqlite3

class ProvidersDal:

    @staticmethod
    def getAddress(name):

        query = "SELECT address FROM Providers WHERE (name='%s')" % name
        connection = sqlite3.connect("barcodeDB.db")
        cursor = connection.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        connection.close()
        return results[1]
    @staticmethod
    def addSender(address, password, provider):
        query = "INSERT INTO SenderMail(address, password, provider) VALUES('%s', '%s', '%s')" %(address,password, provider)
        connection = sqlite3.connect("barcodeDB.db")
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
        cursor.close()
        connection.close()

    @staticmethod
    def getSenders():
        query = "SELECT * FROM SenderMail"
        connection = sqlite3.connect("barcodeDB.db")
        cursor = connection.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        connection.close()
        return results

    @staticmethod
    def removeSender(mail):
        query = "DELETE FROM SenderMail WHERE (address = '%s')" % mail
        connection = sqlite3.connect("barcodeDB.db")
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
        cursor.close()
        connection.close()