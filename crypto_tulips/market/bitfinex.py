from .exchange import Exchange
from crypto_tulips.dal.objects.price_stamp import PriceStamp
from crypto_tulips.dal.services.redis_service import RedisService
import json
import redis


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
        time = int(frame[1] / 1000)
        price = frame[3]
        return PriceStamp("", "bitfinex", time, price)

    @classmethod
    def on_message(self, ws, message):
        msg = json.loads(message)
        if isinstance(msg, list) and msg[1] == "tu":
            # add this to the db
            price_stamp = self.trade_pricestamp_adaptor(msg)
            price_stamp.update_hash()
            rs = RedisService()
            rs.store_object(price_stamp)
            r = rs._connect()
            r.zadd('price_stamps', price_stamp.timestamp, price_stamp.price)



if __name__ == "__main__":
    Bitfinex()
