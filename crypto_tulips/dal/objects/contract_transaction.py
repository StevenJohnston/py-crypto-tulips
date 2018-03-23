"""
Contract Transaction
"""

import json
import time
from crypto_tulips.dal.objects.base_objects.base_transaction import BaseTransaction

class ContractTransaction(BaseTransaction):

    contract_addr = ''
    to_symbol = ''
    from_symbol = ''
    conversion_rate = ''
    # to_symbol value in USD / from_symbol value in USD
    # which gives us 1(to_symbol) == conversion_rate(from_symbol)

    def __init__(self, contract_transaction_hash, signature, from_addr, contract_addr, to_symbol, from_symbol, amount, is_mempool, timestamp = time.time()):
        BaseTransaction.__init__(self, contract_transaction_hash, signature, from_addr, amount, is_mempool, timestamp)

    @staticmethod
    def from_dict(dict_values):
        contract_transaction_hash = dict_values.get('_hash')
        from_addr = dict_values.get('from_addr')
        contract_addr = dict_values.get('contract_addr')
        to_symbol = dict_values.get('to_symbol')
        from_symbol = dict_values.get('from_symbol')
        conversion_rate = dict_values.get('conversion_rate')
        amount = dict_values.get('amount')
        is_mempool = dict_values.get('is_mempool')
        timestamp = dict_values.get('timestamp')
        signature = dict_values.get('signature')
        new_ct = ContractTransaction(contract_transaction_hash, signature, to_addr, from_addr, amount, is_mempool, timestamp)
        new_ct.conversion_rate = conversion_rate
        return new_ct

    @staticmethod
    def _to_index():
        index = super(ContractTransaction, ContractTransaction)._to_index()
        index.append('contract_addr')
        index.append('contract_transaction')
        return index


    def get_signable(self):
        return {
            'from_addr': self.from_addr,
            'contract_addr': self.contract_addr,
            'to_symbol': self.to_symbol,
            'from_symbol': self.from_symbol,
            'amount': "{0:.8f}".format(self.amount),
            'timestamp': self.timestamp
        }

    def get_hashable(self):
        return {
            'signature': self.signature,
            'from_addr': self.from_addr,
            'contract_addr': self.contract_addr,
            'to_symbol': self.to_symbol,
            'from_symbol': self.from_symbol,
            'conversion_rate': "{0:.8f}".format(self.conversion_rate),
            'amount': "{0:.8f}".format(self.amount),
            'timestamp': self.timestamp
        }

    def get_sendable(self):
        return {
            'signature': self.signature,
            'from_addr': self.from_addr,
            'contract_addr': self.contract_addr,
            'to_symbol': self.to_symbol,
            'from_symbol': self.from_symbol,
            'conversion_rate': "{0:.8f}".format(self.conversion_rate),
            'amount': "{0:.8f}".format(self.amount),
            'timestamp': self.timestamp,
            '_hash': self._hash
        }