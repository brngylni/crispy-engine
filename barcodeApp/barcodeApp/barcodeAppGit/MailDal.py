import sqlite3

class MailDal:


    @staticmethod
    def getMails():
        connection = sqlite3.connect("barcodeDB.db")
        cursor = connection.cursor()
        query = "SELECT * FROM Mail"
        cursor.execute(query)
        results =  cursor.fetchall()
        rows = []
        for row in results:
            rows.append(row)
        cursor.close()
        connection.close()
        return rows
    @staticmethod
    def addMail(mail):
        connection = sqlite3.connect("barcodeDB.db")
        cursor = connection.cursor()
        query = "INSERT INTO Mail(Address) VALUES('%s') " % (mail)
        cursor.execute(query)
        connection.commit()
        cursor.close()
        connection.close()
    @staticmethod
    def removeMail(address):
        connection = sqlite3.connect("barcodeDB.db")
        cursor = connection.cursor()
        statement = "DELETE FROM Mail WHERE (Address='%s')" % address
        cursor.execute(statement)
        connection.commit()
        cursor.close()
        connection.close()
    @staticmethod
    def editMail(id, newMail):
        connection = sqlite3.connect("barcodeDB.db")
        cursor = connection.cursor()
        statement = "UPDATE Mail SET Address='%s' WHERE (id=%d)" % (newMail , id)
        cursor.execute(statement)
        connection.commit()
        cursor.close()
        connection.close()

