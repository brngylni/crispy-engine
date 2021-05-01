from binance.client import Client


class BinanceOperations():

    def __init__(self):
        pass

    def buy(self, api_key, api_secret, amount, symbol):
        try:
            client = Client(api_key, api_secret)
            order = client.create_order(
                symbol=symbol,
                side=Client.SIDE_BUY,
                type=Client.ORDER_TYPE_MARKET,
                quoteOrderQty=amount)
            del client
            return True
        except Exception:
            return False

    def sell(self, api_key, api_secret, amount, symbol):
        try:
            client = Client(api_key, api_secret)
            order = client.create_order(
                symbol=symbol,
                side=Client.SIDE_SELL,
                type=Client.ORDER_TYPE_MARKET,
                quantity=amount)
            del client
            return True
        except Exception:
            return False

    def ocoOrder(self, symbol, quantity, price, stopPrice, stopLimitPrice, stopLimitTimeInForce, api_key, api_secret):
        #try:
            client = Client(api_key, api_secret)
            client.order_oco_sell(symbol=symbol, quantity=quantity, price=price, stopPrice=stopPrice,
                              stopLimitPrice=stopLimitPrice, stopLimitTimeInForce=stopLimitTimeInForce)
            del client
            return True
        #except Exception:
         #   return False

    def getPrice(self, symbol, api_key, api_secret):
        client = Client(api_key, api_secret)
        price = client.get_ticker(symbol=symbol)['lastPrice']
        del client
        return price

    def getBalance(self, api_key, api_secret, symbol):
        try:
            client = Client(api_key, api_secret)
            balance = client.get_asset_balance(asset=client.get_symbol_info(symbol)['baseAsset'])['free']
            del client
            return balance
        except Exception:
           return  None


    def getOrders(self, api_key, api_secret):
        client = Client(api_key, api_secret)
        orders = client.get_open_orders()
        del client
        return orders

    def cancelOrder(self, api_key, api_secret, order):
        try:
            client = Client(api_key, api_secret)
            client.cancel_order(symbol=order['symbol'], orderId=order['orderId'])
            del client
            return True
        except Exception:
            return False