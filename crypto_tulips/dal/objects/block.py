# Stored in database with key -> value
#       block:id:actual_hash_here -> block_data
import json
import time

from crypto_tulips.dal.objects.transaction import Transaction
from crypto_tulips.dal.objects.hashable import Hashable
from crypto_tulips.dal.objects.sendable import Sendable

class Block(Hashable, Sendable):
    prefix = 'block'

    block_hash = ''
    transactions = []
    pos_transactions = []
    contract_transactions = []
    timestamp = ''

    def __init__(self, block_hash, transactions, pos_transactions, contract_transactions, timestamp):
        self.block_hash = block_hash
        self.transactions = transactions
        self.pos_transactions = pos_transactions
        self.contract_transactions = contract_transactions
        self.timestamp = timestamp

    @staticmethod
    def from_dict(dict_values):
        block_hash = dict_values.get('block_hash')
        transactions = dict_values.get('transactions')
        pos_transactions = dict_values.get('pos_transactions')
        contract_transactions = dict_values.get('contract_transactions')
        timestamp = dict_values.get('timestamp')
        new_block = Block(block_hash, transactions, pos_transactions, contract_transactions, timestamp)
        return new_block

    def to_string(self):
        return json.dumps(self.__dict__)
        #return str(self.block_hash) + "->" + str(self.block_data)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def _to_index(self):
        return []

    # Returns the object that will be hashed into blockchain
    def hashable(self):
        return {
            'transactions': list(map(Hashable.hashable_callback, self.transactions)),
            'pos_transactions': list(map(Hashable.hashable_callback, self.pos_transactions)),
            'contract_transactions': list(map(Hashable.hashable_callback, self.contract_transactions)),
            'timestamp': self.timestamp
        }

    # Returns the object to be sent around
    def get_sendable(self):
        return {
            'transactions': list(map(Sendable.get_sendable_callback, self.transactions)),
            'pos_transactions': list(map(Sendable.get_sendable_callback, self.pos_transactions)),
            'contract_transactions': list(map(Sendable.get_sendable_callback, self.contract_transactions)),
            'timestamp': self.timestamp,
            'block_hash': self.block_hash
        }

    def from_json(self, json_str):
        self.block_hash = ""
