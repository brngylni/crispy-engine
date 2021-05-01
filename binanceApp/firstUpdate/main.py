import sys
import time
from math import floor

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
        self.ui.btnBuyOco.clicked.connect(self.buyOco)
        self.binance = BinanceOperations()

    def buyOco(self):

        api_key = self.ui.api_key_field.text()
        api_secret = self.ui.api_secret_field.text()
        symbol = self.ui.coin_name_field.text()
        priceMargin = self.ui.price_margin_field.text()
        stopMargin = self.ui.stop_margin_field.text()
        limitMargin = self.ui.limit_margin_field.text()
        price = self.binance.getPrice(symbol, api_key, api_secret)
        old_balance = self.binance.getBalance(api_key, api_secret, symbol)
        self.buy()
        while True:
            time.sleep(0.5)
            balance = self.binance.getBalance(api_key, api_secret, symbol)
            if old_balance != balance:
                break
        oco_price = format((float(priceMargin) * float(price))/100 + float(price), ".7f")
        oco_stop = format(float(price) -  ((float(stopMargin) * float(price))/100), ".7f")
        oco_limit = format(float(price) - ((float(limitMargin) * float(price))/100), ".7f")
        print(f"oco price = {oco_price}, oco stop = {oco_stop}, oco limit = {oco_limit}, balance = {balance}, formatted balance = {format(floor(float(balance)), '.5f')} ")
        QMessageBox.information(self, "Success", "OCO order created") if self.binance.ocoOrder(symbol, format(floor(float(balance)), ".5f"), oco_price, oco_stop, oco_limit, "GTC", api_key, api_secret)\
            else QMessageBox.warning(self,"Error", "An error occured.")



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
        balance = self.binance.getBalance(api_key, api_secret, coin_name)
        for order in self.binance.getOrders(api_key, api_secret):
            try:
                if order['isWorking']:
                    self.binance.cancelOrder(api_key, api_secret, order)
            except:
                continue
        while True:
            if len(self.binance.getOrders(api_key, api_secret)) != 0:
                time.sleep(0.5)
                continue
            break
        QMessageBox.information(self, "Success", "Order Created") if self.binance.sell(api_key, api_secret, floor(float(balance)), coin_name)\
            else QMessageBox.warning(self, "Error", "Something went wrong.")

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.ui.btnBuyOco.click()


app = QtWidgets.QApplication(sys.argv)
win = App()
win.show()
sys.exit(app.exec_())

