"""
Contract Transaction
"""

import json
import time
from crypto_tulips.dal.objects.base_transaction import BaseTransaction

class ContractTransaction(BaseTransaction):

    def __init__(self, contract_transaction_hash, signature, to_addr, from_addr, amount, is_mempool, timestamp = time.time()):
        BaseTransaction.__init__(self, contract_transaction_hash, signature, to_addr, from_addr, amount, is_mempool, timestamp)

    @staticmethod
    def from_dict(dict_values):
        contract_transaction_hash = dict_values.get('_hash')
        to_addr = dict_values.get('to_addr')
        from_addr = dict_values.get('from_addr')
        amount = dict_values.get('amount')
        is_mempool = dict_values.get('is_mempool')
        timestamp = dict_values.get('timestamp')
        signature = dict_values.get('signature')
        new_ct = ContractTransaction(contract_transaction_hash, signature, to_addr, from_addr, amount, is_mempool, timestamp)
        return new_ct

    @staticmethod
    def _to_index():
        index = super(ContractTransaction, ContractTransaction)._to_index()
        index.append('to_addr')
        index.append('contract_transaction')
        return index
