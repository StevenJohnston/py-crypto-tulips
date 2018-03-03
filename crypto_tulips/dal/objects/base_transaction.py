"""
Base Transaction Class
"""

import json
import time
from crypto_tulips.dal.objects.hashable import Hashable
from crypto_tulips.dal.objects.sendable import Sendable

class BaseTransaction(Hashable, Sendable):

    _hash = ''
    to_addr = ''
    from_addr = ''
    amount = ''
    timestamp = ''

    def __init__(self, transaction_hash, to_addr, from_addr, amount, timestamp = time.time()):
        self._hash = transaction_hash
        self.to_addr = to_addr
        self.from_addr = from_addr
        self.amount = float(amount)
        self.timestamp = timestamp

    def to_string(self):
        return json.dumps(self.__dict__)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    @staticmethod
    def _to_index():
        return ['from_addr', 'to_addr']

    # Returns the object that will be hashed into blockchain
    def get_hashable(self): 
        return {
            'to_addr': self.to_addr,
            'from_addr': self.from_addr,
            'amount': self.amount,
            'timestamp': self.timestamp
        }

    def get_sendable(self):
        return {
            'to_addr': self.to_addr,
            'from_addr': self.from_addr,
            'amount': self.amount,
            'timestamp': self.timestamp,
            '_hash': self._hash
        }