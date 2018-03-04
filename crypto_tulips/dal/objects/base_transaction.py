"""
Base Transaction Class
"""

import json
import time
from crypto_tulips.dal.objects.hashable import Hashable
from crypto_tulips.dal.objects.sendable import Sendable
from crypto_tulips.dal.objects.signable import Signable

class BaseTransaction(Hashable, Sendable, Signable):
    to_addr = ''
    from_addr = ''
    amount = ''
    timestamp = ''

    def __init__(self, transaction_hash, signature, to_addr, from_addr, amount, timestamp = time.time()):
        self._hash = transaction_hash
        self.signature = signature
        self.to_addr = to_addr
        self.from_addr = from_addr
        self.amount = float(amount)
        self.timestamp = float(timestamp)

    def to_string(self):
        return json.dumps(self.__dict__)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    @staticmethod
    def _to_index():
        return ['from_addr', 'to_addr']

    def get_signable(self):
        return {
            'to_addr': self.to_addr,
            'from_addr': self.from_addr,
            'amount': self.amount,
            'timestamp': self.timestamp
        }
    # Returns the object that will be hashed into blockchain
    def get_hashable(self):
        return {
            'signature': self.signature,
            'to_addr': self.to_addr,
            'from_addr': self.from_addr,
            'amount': self.amount,
            'timestamp': self.timestamp
        }

    def get_sendable(self):
        return {
            'signature': self.signature,
            'to_addr': self.to_addr,
            'from_addr': self.from_addr,
            'amount': self.amount,
            'timestamp': self.timestamp,
            '_hash': self._hash
        }