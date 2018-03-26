import json
from crypto_tulips.dal.objects.base_objects.hashable import Hashable
from crypto_tulips.dal.objects.base_objects.sendable import Sendable
from crypto_tulips.dal.objects.base_objects.signable import Signable
class PriceStamp(Hashable, Sendable):
    prefix = 'price_stamp'
    price_stamp_hash = ''
    def __init__(self, price_hash, exchange_name, timestamp, price):

        self._hash = price_hash
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

    def to_string(self):
        return json.dumps(self.__dict__)

    @staticmethod
    def _to_index():
        index = ['price_stamp']
        return index

    # Returns the object that will be hashed into blockchain
    def get_hashable(self):
        return {
            'exchange_name': self.exchange_name,
            'timestamp': self.timestamp,
            'price': "{0:.8f}".format(self.price)
        }
    # Returns the object to be sent around
    def get_sendable(self):
        return {
            'exchange_name': self.exchange_name,
            'timestamp': self.timestamp,
            'price': "{0:.8f}".format(self.price),
            '_hash': self._hash
        }