from market.base import Exchange
import json


class Bitfinex(Exchange):

    WEBSOCKET_URL = "wss://api.bitfinex.com/ws/2"
    REST_URL = None
    SUBSCRIBE_TRADES = json.dumps({ 
        "event": "subscribe", 
        "channel": "trades", 
        "symbol": "tBTCUSD",
    })
    @classmethod
    def trade_pricestamp_adaptor(self, data):
        print('bifinex adaptor')
        print(data)
    @classmethod
    def on_message(self, ws, message):
        msg = json.loads(message)
        print('on_message bitfinex')
        print(message)
        print(msg)


if __name__ == "__main__":
    Bitfinex()
  