from binance.client import Client


class BinanceOperations():

    def __init__(self):
        pass

    def buy(self, api_key, api_secret, amount, symbol):
        #try:
            client = Client(api_key, api_secret)
            order = client.create_order(
                symbol=symbol,
                side=Client.SIDE_BUY,
                type=Client.ORDER_TYPE_MARKET,
                quoteOrderQty=amount)
            del client
            return True
       # except Exception:
        #    return False

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

