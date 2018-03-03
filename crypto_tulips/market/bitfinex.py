from .exchange import Exchange
from crypto_tulips.dal.objects.price_stamp import PriceStamp
from crypto_tulips.dal.services.hash_service import HashService
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
        print(msg)
        if isinstance(msg, list) :
            if msg[1] == "tu":
                # add this to the db
                hashService = HashService()
                #hashService.store_hash(self.trade_pricestamp_adaptor(msg))
        


if __name__ == "__main__":
    bitfinex = Bitfinex()
    bitfinex.start()
  