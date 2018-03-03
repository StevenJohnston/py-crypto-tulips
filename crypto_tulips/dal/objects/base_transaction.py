"""
Base Transaction Class
"""

import json
import time

class BaseTransaction:

    _hash = ''
    to_addr = ''
    from_addr = ''
    amount = ''
    timestamp = ''

    def __init__(self, transaction_hash, to_addr, from_addr, amount, timestamp = time.strftime("%Y/%m/%d-%H:%M:%S")):
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