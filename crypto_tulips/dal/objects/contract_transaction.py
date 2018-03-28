"""
Contract Transaction
"""

import json
import time
from crypto_tulips.dal.objects.base_objects.base_transaction import BaseTransaction

class ContractTransaction(BaseTransaction):

    signed_contract_addr = ''
    to_symbol = ''
    from_symbol = ''
    price = ''

    def __init__(self, contract_transaction_hash, signature, from_addr, signed_contract_addr, to_symbol, from_symbol, amount, price, is_mempool, timestamp = time.time()):
        BaseTransaction.__init__(self, contract_transaction_hash, signature, from_addr, amount, is_mempool, timestamp)
        self.signed_contract_addr = signed_contract_addr
        self.to_symbol = to_symbol
        self.from_symbol = from_symbol
        self.price = float(price)

    @staticmethod
    def from_dict(dict_values):
        contract_transaction_hash = dict_values.get('_hash')
        from_addr = dict_values.get('from_addr')
        signed_contract_addr = dict_values.get('signed_contract_addr')
        to_symbol = dict_values.get('to_symbol')
        from_symbol = dict_values.get('from_symbol')
        price = dict_values.get('price')
        amount = dict_values.get('amount')
        is_mempool = dict_values.get('is_mempool')
        timestamp = dict_values.get('timestamp')
        signature = dict_values.get('signature')
        new_ct = ContractTransaction(contract_transaction_hash, signature, from_addr, \
                signed_contract_addr, to_symbol, from_symbol, amount, price, is_mempool, timestamp)
        return new_ct

    @staticmethod
    def _to_index():
        index = super(ContractTransaction, ContractTransaction)._to_index()
        index.append('signed_contract_addr')
        index.append('contract_transaction')
        return index


    def get_signable(self):
        return {
            'from_addr': self.from_addr,
            'signed_contract_addr': self.signed_contract_addr,
            'to_symbol': self.to_symbol,
            'from_symbol': self.from_symbol,
            'price': "{0:.8f}".format(self.price),
            'amount': "{0:.8f}".format(self.amount),
            'timestamp': self.timestamp
        }

    def get_hashable(self):
        return {
            'signature': self.signature,
            'from_addr': self.from_addr,
            'signed_contract_addr': self.signed_contract_addr,
            'to_symbol': self.to_symbol,
            'from_symbol': self.from_symbol,
            'price': "{0:.8f}".format(self.price),
            'amount': "{0:.8f}".format(self.amount),
            'timestamp': self.timestamp
        }

    def get_sendable(self):
        return {
            'signature': self.signature,
            'from_addr': self.from_addr,
            'signed_contract_addr': self.signed_contract_addr,
            'to_symbol': self.to_symbol,
            'from_symbol': self.from_symbol,
            'price': "{0:.8f}".format(self.price),
            'amount': "{0:.8f}".format(self.amount),
            'timestamp': self.timestamp,
            '_hash': self._hash
        }
