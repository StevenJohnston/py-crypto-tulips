"""
PosTransaction Class
"""

import json
import time
from crypto_tulips.dal.objects.hashable import Hashable
from crypto_tulips.dal.objects.sendable import Sendable

class PosTransaction(Hashable):

    def __init__(self, pos_transaction_hash, addr, amount, timestamp = time.time()):
        self._hash = pos_transaction_hash
        self.addr = addr
        self.amount = amount
        self.timestamp = timestamp

    @staticmethod
    def from_dict(dict_values):
        pos_transaction_hash = dict_values.get('_hash')
        addr = dict_values.get('addr')
        amount = dict_values.get('amount')
        timestamp = dict_values.get('timestamp')
        pos_transaction = PosTransaction(pos_transaction_hash, addr, amount, timestamp)
        return pos_transaction

    @staticmethod
    def _to_index():
        return []

    # Returns the object that will be hashed into blockchain
    def get_hashable(self):
        return {
            'addr': self.addr,
            'amount': self.amount,
            'timestamp': self.timestamp
        }

    # Returns the object to be sent around
    def get_sendable(self):
        return {
            'addr': self.addr,
            'amount': self.amount,
            'timestamp': self.timestamp,
            '_hash': self._hash
        }