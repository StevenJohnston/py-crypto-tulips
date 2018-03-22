"""
Base Transaction Class
"""

import json
import time
from crypto_tulips.dal.objects.base_objects.hashable import Hashable
from crypto_tulips.dal.objects.base_objects.sendable import Sendable
from crypto_tulips.dal.objects.base_objects.signable import Signable

class BaseTransaction(Hashable, Sendable, Signable):
    from_addr = ''
    amount = ''
    timestamp = ''
    is_mempool = ''

    def __init__(self, transaction_hash, signature, from_addr, amount, is_mempool = 1, timestamp = time.time()):
        self._hash = transaction_hash
        self.signature = signature
        self.from_addr = from_addr
        self.amount = float(amount)
        if is_mempool == None:
            is_mempool = 1
        self.is_mempool = int(is_mempool)
        self.timestamp = int(timestamp)

    def to_string(self):
        return json.dumps(self.__dict__, sort_keys=True, separators=(',', ':'))

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    @staticmethod
    def _to_index():
        return ['from_addr', 'is_mempool']

    def get_public_key(self):
        return self.from_addr

    def get_signable(self):
        return {
            'from_addr': self.from_addr,
            'amount': "{0:.8f}".format(self.amount),
            'timestamp': self.timestamp
        }

    # Returns the object that will be hashed into blockchain
    def get_hashable(self):
        return {
            'signature': self.signature,
            'from_addr': self.from_addr,
            'amount': "{0:.8f}".format(self.amount),
            'timestamp': self.timestamp
        }

    def get_sendable(self):
        return {
            'signature': self.signature,
            'from_addr': self.from_addr,
            'amount': "{0:.8f}".format(self.amount),
            'timestamp': self.timestamp,
            '_hash': self._hash
        }