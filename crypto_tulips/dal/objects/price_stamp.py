import json
class PriceStamp:
    def __init__(self, exchange, timestamp, price):
        self.exchange = exchange
        self.timestamp = timestamp
        self.price = price

    def to_string(self):
        return json.dumps(self.__dict__)