"""
Contract Class
"""

import json
import time
from crypto_tulips.dal.objects.base_objects.hashable import Hashable
from crypto_tulips.dal.objects.base_objects.sendable import Sendable
from crypto_tulips.dal.objects.base_objects.signable import Signable

class Contract(Hashable, Sendable, Signable):
    _hash = ''
    signature = ''
    to_addr = ''
    from_addr = ''
    amount = ''
    is_mempool = ''
    duration = ''
    timestamp = ''

    def __init__(self, contract_hash, signature, to_addr, from_addr, is_mempool, duration, timestamp = time.time()):
        self._hash = contract_hash
        self.signature = signature
        self.to_addr = to_addr
        self.from_addr = from_addr
        self.amount = amount
        self.is_mempool = is_mempool
        self.duration = int(duration)
        self.timestamp = int(timestamp)

    @staticmethod
    def from_dict(dict_values):
        contract_hash = dict_values.get('_hash')
        signature = dict_values.get('signature')
        to_addr = dict_values.get('to_addr')
        from_addr = dict_values.get('from_addr')
        amount = dict_values.get('amount')
        is_mempool = dict_values.get('is_mempool')
        duration = dict_values.get('duration')
        timestamp = dict_values.get('timestamp')
        new_contract = Contract(contract_hash, signature, to_addr, from_addr, is_mempool, duration, timestamp)
        return new_contract

    def get_public_key(self):
        return self.from_addr

    def get_signable(self):
        return {
            'to_addr': self.to_addr,
            'from_addr': self.from_addr,
            'amount': self.amount,
            'duration': self.duration,
            'timestamp': self.timestamp
        }
    
    def get_hashable(self):
        return {
            'signature': self.signature,
            'to_addr': self.to_addr,
            'from_addr': self.from_addr,
            'amount': self.amount,
            'duration': self.duration,
            'timestamp': self.timestamp
        }

    def get_sendable(self):
        return {
            'signature': self.signature,
            'to_addr': self.to_addr,
            'from_addr': self.from_addr,
            'amount': self.amount,
            'duration': self.duration,
            'timestamp': self.timestamp
            '_hash': self._hash
        }

    @staticmethod
    def _to_index():
        return ['to_addr', 'from_addr', 'is_mempool', 'contract']