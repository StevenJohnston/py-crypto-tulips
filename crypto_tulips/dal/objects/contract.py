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
    owner = ''
    amount = ''
    rate = ''
    is_mempool = ''
    duration = ''
    created_timestamp = ''
    sign_end_timestamp = ''

    def __init__(self, contract_hash, signature, owner, amount, rate, is_mempool, duration, created_timestamp, sign_end_timestamp):
        self._hash = contract_hash
        self.signature = signature

        self.owner = owner
        self.amount = float(amount)
        self.rate = float(rate)
        self.is_mempool = int(is_mempool)
        self.duration = int(duration)
        self.created_timestamp = int(created_timestamp)
        self.sign_end_timestamp = int(sign_end_timestamp)

    @staticmethod
    def from_dict(dict_values):
        contract_hash = dict_values.get('_hash')
        signature = dict_values.get('signature')

        owner = dict_values.get('owner')
        amount = dict_values.get('amount')
        rate = dict_values.get('rate')
        is_mempool = dict_values.get('is_mempool')

        duration = dict_values.get('duration')
        created_timestamp = dict_values.get('created_timestamp')
        sign_end_timestamp = dict_values.get('sign_end_timestamp')

        new_contract = Contract(contract_hash, signature, owner, amount, rate, is_mempool, duration, created_timestamp, sign_end_timestamp)
        return new_contract

    def get_public_key(self):
        return self._hash

    def get_signable(self):
        return {
            'owner': self.owner,
            'amount': "{0:.8f}".format(self.amount),
            'rate': "{0:.8f}".format(self.rate),
            'duration': self.duration,
            'created_timestamp': self.created_timestamp,
            'sign_end_timestamp': self.sign_end_timestamp
        }

    def get_hashable(self):
        return {
            'signature': self.signature,
            'owner': self.owner,
            'amount': "{0:.8f}".format(self.amount),
            'rate': "{0:.8f}".format(self.rate),
            'duration': self.duration,
            'created_timestamp': self.created_timestamp,
            'sign_end_timestamp': self.sign_end_timestamp
        }

    def get_sendable(self):
        return {
            'signature': self.signature,
            'owner': self.owner,
            'amount': "{0:.8f}".format(self.amount),
            'rate': "{0:.8f}".format(self.rate),
            'duration': self.duration,
            'created_timestamp': self.created_timestamp,
            'sign_end_timestamp': self.sign_end_timestamp,
            '_hash': self._hash
        }

    @staticmethod
    def _to_index():
        return ['owner', 'is_mempool', 'contract']