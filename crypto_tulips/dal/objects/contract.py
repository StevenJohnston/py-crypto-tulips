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
    addr = ''
    owner = ''
    amount = ''
    rate = ''
    is_mempool = ''
    duration = ''
    timestamp = ''
    end_timestamp = ''

    def __init__(self, contract_hash, signature, addr, owner, amount, rate, is_mempool, duration, timestamp = time.time(), end_timestamp = None):
        self._hash = contract_hash
        self.signature = signature
        self.addr = addr
        self.owner = owner
        self.amount = amount
        self.rate = rate
        self.is_mempool = is_mempool
        self.duration = int(duration)
        self.timestamp = int(timestamp)
        if end_timestamp == None:
            self.end_timestamp = self.timestamp + self.duration
        else:
            self.end_timestamp = end_timestamp

    @staticmethod
    def from_dict(dict_values):
        contract_hash = dict_values.get('_hash')
        signature = dict_values.get('signature')
        addr = dict_values.get('addr')
        owner = dict_values.get('owner')
        amount = dict_values.get('amount')
        rate = dict_values.get('rate')
        is_mempool = dict_values.get('is_mempool')
        duration = dict_values.get('duration')
        timestamp = dict_values.get('timestamp')
        end_timestamp = dict_values.get('end_timestamp')
        new_contract = Contract(contract_hash, signature, addr, owner, is_mempool, duration, timestamp, end_timestamp)
        return new_contract

    def get_public_key(self):
        return self._hash

    def get_signable(self):
        return {
            'addr': self.addr,
            'owner': self.owner,
            'amount': "{0:.8f}".format(self.amount),
            'rate': "{0:.8f}".format(self.rate),
            'duration': self.duration,
            'timestamp': self.timestamp,
            'end_timestamp': self.end_timestamp
        }

    def get_hashable(self):
        return {
            'signature': self.signature,
            'addr': self.addr,
            'owner': self.owner,
            'amount': "{0:.8f}".format(self.amount),
            'rate': "{0:.8f}".format(self.rate),
            'duration': self.duration,
            'timestamp': self.timestamp,
            'end_timestamp': self.end_timestamp
        }

    def get_sendable(self):
        return {
            'signature': self.signature,
            'owner': self.owner,
            'addr': self.addr,
            'amount': "{0:.8f}".format(self.amount),
            'rate': "{0:.8f}".format(self.rate),
            'duration': self.duration,
            'timestamp': self.timestamp,
            'end_timestamp': self.end_timestamp,
            '_hash': self._hash
        }

    @staticmethod
    def _to_index():
        return ['addr', 'owner', 'is_mempool', 'contract']