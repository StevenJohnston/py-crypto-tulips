from .exchange import Exchange
from crypto_tulips.dal.objects.price_stamp import PriceStamp
<<<<<<< HEAD
from crypto_tulips.dal.services.hash_service import HashService
=======
>>>>>>> a27cfd09d3316388877cba22ddf6a9c0288c60e8
import json


class Bitfinex(Exchange):
<<<<<<< HEAD
=======

>>>>>>> a27cfd09d3316388877cba22ddf6a9c0288c60e8
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
<<<<<<< HEAD
        print(msg)
        if isinstance(msg, list) :
            if msg[1] == "tu":
                # add this to the db
                hashService = HashService()
                #hashService.store_hash(self.trade_pricestamp_adaptor(msg))
=======
        if msg[1] == "tu":
            # add this to the db
            self.trade_pricestamp_adaptor(msg)
>>>>>>> a27cfd09d3316388877cba22ddf6a9c0288c60e8
        


if __name__ == "__main__":
<<<<<<< HEAD
    bitfinex = Bitfinex()
    bitfinex.start()
=======
    Bitfinex()
>>>>>>> a27cfd09d3316388877cba22ddf6a9c0288c60e8
  