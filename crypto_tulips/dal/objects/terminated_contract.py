"""
Terminated Contract Class
"""

import json
from crypto_tulips.dal.objects.base_objects.hashable import Hashable
from crypto_tulips.dal.objects.base_objects.sendable import Sendable
from crypto_tulips.dal.objects.base_objects.signable import Signable

class TerminatedContract(Sendable):

    _hash = ''
    price = ''
    timestamp = ''

    def __init__(self, signed_contract_hash, price, timestamp):
        self._hash = signed_contract_hash
        self.price = float(price)
        self.timestamp = int(timestamp)

    @staticmethod
    def from_dict(dict_values):
        signed_contract_hash = dict_values.get('_hash')
        price = dict_values.get('price')
        timestamp = dict_values.get('timestamp')
        tc = TerminatedContract(signed_contract_hash, price, timestamp)
        return tc

    def get_sendable(self):
        return {
            'price': self.price,
            'timestamp': self.timestamp,
            '_hash': self._hash
        }

    @staticmethod
    def _to_index():
        return ['terminated_contract']