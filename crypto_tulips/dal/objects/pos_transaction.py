"""
PosTransaction Class
"""

import json
import time
from crypto_tulips.dal.objects.base_objects.base_transaction import BaseTransaction

class PosTransaction(BaseTransaction):

    def __init__(self, pos_transaction_hash, signature, addr, amount, is_mempool, timestamp = time.time()):
        BaseTransaction.__init__(self, pos_transaction_hash, signature, None, addr, amount, is_mempool, timestamp)

    @staticmethod
    def from_dict(dict_values):
        pos_transaction_hash = dict_values.get('_hash')
        from_addr = dict_values.get('from_addr')
        amount = dict_values.get('amount')
        is_mempool = dict_values.get('is_mempool')
        timestamp = dict_values.get('timestamp')
        signature = dict_values.get('signature')
        pos_transaction = PosTransaction(pos_transaction_hash, signature, from_addr, amount, is_mempool, timestamp)
        return pos_transaction

    @staticmethod
    def _to_index():
        return ['pos_transaction']

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

    # Returns the object to be sent around
    def get_sendable(self):
        return {
            'signature': self.signature,
            'from_addr': self.from_addr,
            'amount': "{0:.8f}".format(self.amount),
            'timestamp': self.timestamp,
            '_hash': self._hash
        }
