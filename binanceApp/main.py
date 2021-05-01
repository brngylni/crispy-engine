import sys

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox

from BinanceOperations import BinanceOperations
from MainWindow import Ui_MainWindow


class App(QtWidgets.QMainWindow):

    def __init__(self):
        super(App, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.btnBuy.clicked.connect(self.buy)
        self.ui.btnSell.clicked.connect(self.sell)
        self.binance = BinanceOperations()

    def buy(self):
        api_key = self.ui.api_key_field.text()
        api_secret = self.ui.api_secret_field.text()
        coin_name = self.ui.coin_name_field.text()
        coin_amount = self.ui.coin_amount_field.text()
        QMessageBox.information(self, "Success", "Order Created") if self.binance.buy(api_key, api_secret,coin_amount,
                                                                                       coin_name) \
            else QMessageBox.warning(self, "Error", "Something went wrong.")

    def sell(self):
        api_key = self.ui.api_key_field.text()
        api_secret = self.ui.api_secret_field.text()
        coin_name = self.ui.coin_name_field.text()
        coin_amount = self.ui.coin_amount_field.text()
        QMessageBox.information(self, "Success", "Order Created") if self.binance.sell(api_key, api_secret, coin_amount, coin_name)\
            else QMessageBox.warning(self, "Error", "Something went wrong.")

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.ui.btnBuy.click()


app = QtWidgets.QApplication(sys.argv)
win = App()
win.show()
sys.exit(app.exec_())

