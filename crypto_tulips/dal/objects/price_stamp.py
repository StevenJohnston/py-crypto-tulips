import json
class PriceStamp:
<<<<<<< HEAD
    prefix = 'price_stamp'
    price_stamp_hash = ''
    def __init__(self, price_hash, exchange_name, timestamp, price):
        
        self.exchange_name = exchange_name
        self.timestamp = timestamp
        self.price = price

    @staticmethod
    def from_dict(dict_values):
        price_hash = dict_values.get('price_hash')
        exchange_name = dict_values.get('exchange_name')
        timestamp = dict_values.get('timestamp')
        price = dict_values.get('price')
        new_price_stamp = PriceStamp(price_hash, exchange_name, timestamp, price)
        return new_price_stamp

=======
    def __init__(self, exchange, timestamp, price):
        self.exchange = exchange
        self.timestamp = timestamp
        self.price = price

>>>>>>> a27cfd09d3316388877cba22ddf6a9c0288c60e8
    def to_string(self):
        return json.dumps(self.__dict__)