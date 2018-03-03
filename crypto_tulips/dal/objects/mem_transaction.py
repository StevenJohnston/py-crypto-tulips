"""
MemTransaction Class
"""

import json
import time
from .base_transaction import BaseTransaction

class MemTransaction(BaseTransaction):

    def __init__(self, mem_transaction_hash, to_addr, from_addr, amount, timestamp = time.strftime("%Y/%m/%d-%H:%M:%S")):
        BaseTransaction.__init__(self, mem_transaction_hash, to_addr, from_addr, amount, timestamp)

    @staticmethod
    def from_dict(dict_values):
        mem_transaction_hash = dict_values.get('_hash')
        to_addr = dict_values.get('to_addr')
        from_addr = dict_values.get('from_addr')
        amount = dict_values.get('amount')
        timestamp = dict_values.get('timestamp')
        # print(mem_transaction_hash, to_addr, from_addr, str(amount), timestamp)
        mem_transaction = MemTransaction(mem_transaction_hash, to_addr, from_addr, amount, timestamp)
        return mem_transaction

    @staticmethod
    def _to_index():
        fields = super(MemTransaction, MemTransaction)._to_index()
        fields.append('mem_transaction')
        return fields