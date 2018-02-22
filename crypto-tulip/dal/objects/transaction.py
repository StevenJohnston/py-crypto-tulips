"""
Transaction Class
"""

import json
import time

class Transaction:

    prefix = "transaction"

    transaction_hash = ''
    to_addr = ''
    from_addr = ''
    amount = ''
    timestamp = ''

    def __init__(self, transaction_hash, to_addr, from_addr, amount, timestamp = time.strftime("%Y/%m/%d-%H:%M:%S")):
        self.transaction_hash = transaction_hash
        self.to_addr = to_addr
        self.from_addr = from_addr
        self.amount = float(amount)
        self.timestamp = timestamp

    @staticmethod
    def from_dict(dict_values):
        transaction_hash = dict_values.get('transaction_hash')
        to_addr = dict_values.get('to_addr')
        from_addr = dict_values.get('from_addr')
        amount = dict_values.get('amount')
        timestamp = dict_values.get('timestamp')
        new_transaction = Transaction(transaction_hash, to_addr, from_addr, amount, timestamp)
        return new_transaction

    def to_string(self):
        return json.dumps(self.__dict__)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__
