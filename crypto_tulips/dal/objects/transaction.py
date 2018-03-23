"""
Transaction Class
"""

import json
import time
from crypto_tulips.dal.objects.base_objects.base_transaction import BaseTransaction

class Transaction(BaseTransaction):

    to_addr = ''

    def __init__(self, transaction_hash, signature, to_addr, from_addr, amount, is_mempool, timestamp = time.time()):
        self.to_addr = to_addr
        BaseTransaction.__init__(self, transaction_hash, signature, from_addr, amount, is_mempool, timestamp)

    @staticmethod
    def from_dict(dict_values):
        transaction_hash = dict_values.get('_hash')
        to_addr = dict_values.get('to_addr')
        from_addr = dict_values.get('from_addr')
        amount = dict_values.get('amount')
        timestamp = dict_values.get('timestamp')
        signature = dict_values.get('signature')
        is_mempool = dict_values.get('is_mempool')
        new_transaction = Transaction(transaction_hash, signature, to_addr, from_addr, amount, is_mempool, timestamp)
        return new_transaction

    @staticmethod
    def _to_index():
        index = super(Transaction, Transaction)._to_index()
        index.append('to_addr')
        index.append('transaction')
        return index


    def get_signable(self):
        return {
            'to_addr': self.to_addr,
            'from_addr': self.from_addr,
            'amount': "{0:.8f}".format(self.amount),
            'timestamp': self.timestamp
        }

    # Returns the object that will be hashed into blockchain
    def get_hashable(self):
        return {
            'signature': self.signature,
            'to_addr': self.to_addr,
            'from_addr': self.from_addr,
            'amount': "{0:.8f}".format(self.amount),
            'timestamp': self.timestamp
        }

    def get_sendable(self):
        return {
            'signature': self.signature,
            'to_addr': self.to_addr,
            'from_addr': self.from_addr,
            'amount': "{0:.8f}".format(self.amount),
            'timestamp': self.timestamp,
            '_hash': self._hash
        }