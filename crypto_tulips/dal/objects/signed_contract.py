"""
Signed Contract Class
"""

import json
import time
from crypto_tulips.dal.objects.base_objects.hashable import Hashable
from crypto_tulips.dal.objects.base_objects.sendable import Sendable
from crypto_tulips.dal.objects.base_objects.signable import Signable

class SignedContract(Hashable, Sendable, Signable):
    _hash = ''
    signature = ''
    from_addr = ''
    signed_timestamp = ''

    parent_hash = ''
    parent_signature = ''
    parent_owner = ''

    amount = ''
    rate = ''
    is_mempool = ''
    duration = ''
    created_timestamp = ''
    sign_end_timestamp = ''
    def __init__(self, sc_hash, sc_signature, sc_from_addr, signed_timestamp, parent_hash, parent_signature, parent_owner, amount, rate, is_mempool, duration, created_timestamp, sign_end_timestamp):
        self._hash = sc_hash
        self.signature = sc_signature
        self.from_addr = sc_from_addr
        self.signed_timestamp = int(signed_timestamp)

        self.parent_hash = parent_hash
        self.parent_signature = parent_signature
        self.parent_owner = parent_owner

        self.amount = float(amount)
        self.rate = float(rate)
        self.is_mempool = 1 if is_mempool is None else int(is_mempool)
        self.duration = int(duration)
        self.created_timestamp = int(created_timestamp)
        self.sign_end_timestamp = int(sign_end_timestamp)

    @staticmethod
    def from_dict(dict_values):
        _hash = dict_values.get('_hash')
        signature = dict_values.get('signature')
        from_addr = dict_values.get('from_addr')
        signed_timestamp = dict_values.get('signed_timestamp')

        parent_hash = dict_values.get('parent_hash')
        parent_signature = dict_values.get('parent_signature')
        parent_owner = dict_values.get('parent_owner')

        amount = dict_values.get('amount')
        rate = dict_values.get('rate')
        is_mempool = dict_values.get('is_mempool')
        duration = dict_values.get('duration')
        created_timestamp = dict_values.get('created_timestamp')
        sign_end_timestamp = dict_values.get('sign_end_timestamp')
        sc = SignedContract(_hash, signature, from_addr, signed_timestamp, parent_hash, parent_signature, parent_owner, amount, rate, is_mempool, duration, created_timestamp, sign_end_timestamp)
        return sc

    def get_public_key(self):
        return self._hash

    def get_signable(self):
        return {
            'from_addr': self.from_addr,
            'signed_timestamp': self.signed_timestamp,
            'parent_hash': self.parent_hash,
            'parent_signature': self.parent_signature,
            'parent_owner': self.parent_owner,
            'amount': self.amount,
            'rate': self.rate,
            'is_mempool': self.is_mempool,
            'duration': self.duration,
            'created_timestamp': self.created_timestamp,
            'sign_end_timestamp': self.sign_end_timestamp
        }

    def get_hashable(self):
        return {
            'signature': self.signature,
            'from_addr': self.from_addr,
            'signed_timestamp': self.signed_timestamp,
            'parent_hash': self.parent_hash,
            'parent_signature': self.parent_signature,
            'parent_owner': self.parent_owner,
            'amount': self.amount,
            'rate': self.rate,
            'is_mempool': self.is_mempool,
            'duration': self.duration,
            'created_timestamp': self.created_timestamp,
            'sign_end_timestamp': self.sign_end_timestamp
        }

    def get_sendable(self):
        return {
            'signature': self.signature,
            'from_addr': self.from_addr,
            'signed_timestamp': self.signed_timestamp,
            'parent_hash': self.parent_hash,
            'parent_signature': self.parent_signature,
            'parent_owner': self.parent_owner,
            'amount': self.amount,
            'rate': self.rate,
            'is_mempool': self.is_mempool,
            'duration': self.duration,
            'created_timestamp': self.created_timestamp,
            'sign_end_timestamp': self.sign_end_timestamp,
            '_hash': self._hash
        }

    @staticmethod
    def _to_index():
        return ['from_addr', 'parent_hash', 'is_mempool', 'signed_contract']
