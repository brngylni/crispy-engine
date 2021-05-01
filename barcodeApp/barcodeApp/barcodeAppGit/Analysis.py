import matplotlib.pyplot as plt
import sqlite3

from PyQt5.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.backends.backend_template import FigureCanvas
from matplotlib.figure import Figure


class Analysis():



    @staticmethod
    def analyse():
        connection = sqlite3.connect("barcodeDB.db")
        cursor = connection.cursor()
        query = "SELECT * FROM Products ORDER BY sold DESC"
        cursor.execute(query)
        results = cursor.fetchall()
        names = []
        rates = []
        plt.rcParams["font.size"] = "5"
        for i in range(0,20):
            if i == len(results):
                break
            names.append(str(results[i][6]))
            rates.append(results[i][4])
        fig = plt.figure()
        plt.bar(names, rates, color='maroon',)
        plt.xlabel("Names")
        plt.ylabel("Total Sales")
        plt.title("Sale Chart")
        plt.draw()

        plt.savefig("saleRates.png")

