from .exchange import Exchange
from crypto_tulips.dal.objects.price_stamp import PriceStamp
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
        frame = data[2]
        time = frame[1]
        price = frame[3]
        return PriceStamp("bitfinex", time, price)
    @classmethod
    def on_message(self, ws, message):
        msg = json.loads(message)
        if msg[1] == "tu":
            # add this to the db
            self.trade_pricestamp_adaptor(msg)
        


if __name__ == "__main__":
    Bitfinex()
  