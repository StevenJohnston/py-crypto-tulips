"""
Transaction Class
"""

import json
import time
from crypto_tulips.dal.objects.base_transaction import BaseTransaction

class Transaction(BaseTransaction):

    def __init__(self, transaction_hash, to_addr, from_addr, amount, timestamp = time.time()):
        BaseTransaction.__init__(self, transaction_hash, to_addr, from_addr, amount, timestamp)

    @staticmethod
    def from_dict(dict_values):
        transaction_hash = dict_values.get('_hash')
        to_addr = dict_values.get('to_addr')
        from_addr = dict_values.get('from_addr')
        amount = dict_values.get('amount')
        timestamp = dict_values.get('timestamp')
        new_transaction = Transaction(transaction_hash, to_addr, from_addr, amount, timestamp)
        return new_transaction

    @staticmethod
    def _to_index():
        fields = super(Transaction, Transaction)._to_index()
        fields.append('transaction')
        return fields
