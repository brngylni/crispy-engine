import sqlite3

class GroupsDal:

    @staticmethod
    def getGroups():

        connection = sqlite3.connect("barcodeDB.db")
        cursor = connection.cursor()
        query = "SELECT * FROM Groups"
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        connection.close()
        return(results)

    @staticmethod
    def addCompanie(companie):
        connection = sqlite3.connect("barcodeDB.db")
        cursor = connection.cursor()
        query = "INSERT INTO Groups(name) VALUES ('%s')" % companie
        cursor.execute(query)
        connection.commit()
        cursor.close()
        connection.close()

    @staticmethod
    def removeCompany(name):
        connection = sqlite3.connect("barcodeDB.db")
        cursor = connection.cursor()
        query = "DELETE FROM Groups WHERE(name='%s')" % name
        cursor.execute(query)
        connection.commit()
        cursor.close()
        connection.close()