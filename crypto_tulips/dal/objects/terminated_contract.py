"""
Terminated Contract Class
"""

import json
from crypto_tulips.dal.objects.base_objects.hashable import Hashable
from crypto_tulips.dal.objects.base_objects.sendable import Sendable
from crypto_tulips.dal.objects.base_objects.signable import Signable

class TerminatedContract(Sendable):

    _hash = ''
    signed_contract_addr = ''
    price = ''
    timestamp = ''

    def __init__(self, signed_contract_hash, signed_contract_addr, price, timestamp):
        self._hash = signed_contract_hash
        self.signed_contract_addr = signed_contract_addr
        self.price = price
        self.timestamp = timestamp

    @staticmethod
    def from_dict(dict_values):
        contract_hash = dict_values.get('_hash')
        signed_contract_addr = dict_values.get('signed_contract_addr')
        price = dict_values.get('price')
        timestamp = dict_values.get('timestamp')
        tc = TerminatedContract(contract_hash, signed_contract_addr, price, timestamp)
        return tc

    def get_sendable(self):
        return {
            'signed_contract_addr': self.signed_contract_addr,
            'price': self.price,
            'timestamp': self.timestamp,
            '_hash': self._hash
        }

    @staticmethod
    def _to_index():
        return ['signed_contract_addr', 'terminated_contract']