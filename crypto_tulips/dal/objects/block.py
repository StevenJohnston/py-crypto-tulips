# Stored in database with key -> value
#       block:id:actual_hash_here -> block_data
import json
import time

from crypto_tulips.dal.objects.transaction import Transaction
from crypto_tulips.dal.objects.pos_transaction import PosTransaction
from crypto_tulips.dal.objects.contract_transaction import ContractTransaction
from crypto_tulips.dal.objects.contract import Contract
from crypto_tulips.dal.objects.signed_contract import SignedContract
from crypto_tulips.dal.objects.terminated_contract import TerminatedContract

from crypto_tulips.dal.objects.base_objects.hashable import Hashable
from crypto_tulips.dal.objects.base_objects.sendable import Sendable
from crypto_tulips.dal.objects.base_objects.signable import Signable

class Block(Hashable, Sendable, Signable):
    prefix = 'block'
    transactions = []
    pos_transactions = []
    contract_transactions = []
    contracts = []
    signed_contracts = []
    terminated_contracts = []
    timestamp = ''
    owner = ''
    height = 0
    prev_block = ''

    def __init__(self, block_hash, signature, owner, prev_block, height, transactions, pos_transactions, contract_transactions, contracts, signed_contracts, terminated_contracts, timestamp = time.time()):
        self._hash = block_hash
        self.signature = signature
        self.owner = owner
        self.height = int(height)
        self.transactions = transactions
        self.pos_transactions = pos_transactions
        self.contract_transactions = contract_transactions
        self.contracts = contracts
        self.signed_contracts = signed_contracts
        self.terminated_contracts = terminated_contracts
        self.timestamp = int(timestamp)
        self.prev_block = prev_block

    @staticmethod
    def from_dict(dict_values):
        block_hash = dict_values.get('_hash')
        signature = dict_values.get('signature')
        owner = dict_values.get('owner')
        height = dict_values.get('height')
        transactions = list(map(Transaction.from_dict, dict_values.get('transactions')))
        pos_transactions = list(map(PosTransaction.from_dict, dict_values.get('pos_transactions')))
        contract_transactions = list(map(ContractTransaction.from_dict, dict_values.get('contract_transactions')))
        contracts = list(map(Contract.from_dict, dict_values.get('contracts')))
        signed_contracts = list(map(SignedContract.from_dict, dict_values.get('signed_contracts')))
        terminated_contracts = list(map(TerminatedContract.from_dict, dict_values.get('terminated_contracts')))
        timestamp = dict_values.get('timestamp')
        prev_block = dict_values.get('prev_block')
        new_block = Block(block_hash, signature, owner, prev_block, height, transactions, pos_transactions, contract_transactions, contracts, signed_contracts, terminated_contracts, timestamp)
        return new_block

    def to_string(self):
        return json.dumps(self.__dict__, sort_keys=True, separators=(',', ':'))
        #return str(self.block_hash) + "->" + str(self.block_data)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def get_public_key(self):
        return self.owner

    def get_signable(self):
        return {
            'prev_block': self.prev_block,
            'height': self.height,
            'transactions': list(map(Signable.get_signable_callback, self.transactions)),
            'pos_transactions': list(map(Signable.get_signable_callback, self.pos_transactions)),
            'contract_transactions': list(map(Signable.get_signable_callback, self.contract_transactions)),
            'contracts': list(map(Signable.get_signable_callback, self.contracts)),
            'signed_contracts': list(map(Signable.get_signable_callback, self.signed_contracts)),
            'terminated_contracts': list(map(Sendable.get_sendable_callback, self.terminated_contracts)),
            'timestamp': self.timestamp
        }

    # Returns the object that will be hashed into blockchain
    def get_hashable(self):
        return {
            'signature': self.signature,
            'owner': self.owner,
            'prev_block': self.prev_block,
            'height': self.height,
            'transactions': list(map(Sendable.get_sendable_callback, self.transactions)),
            'pos_transactions': list(map(Sendable.get_sendable_callback, self.pos_transactions)),
            'contract_transactions': list(map(Sendable.get_sendable_callback, self.contract_transactions)),
            'contracts': list(map(Sendable.get_sendable_callback, self.contracts)),
            'signed_contracts': list(map(Sendable.get_sendable_callback, self.signed_contracts)),
            'terminated_contracts': list(map(Sendable.get_sendable_callback, self.terminated_contracts)),
            'timestamp': self.timestamp
        }

    # Returns the object to be sent around
    def get_sendable(self):
        return {
            'signature': self.signature,
            'owner': self.owner,
            'prev_block': self.prev_block,
            'height': self.height,
            'transactions': list(map(Sendable.get_sendable_callback, self.transactions)),
            'pos_transactions': list(map(Sendable.get_sendable_callback, self.pos_transactions)),
            'contract_transactions': list(map(Sendable.get_sendable_callback, self.contract_transactions)),
            'contracts': list(map(Sendable.get_sendable_callback, self.contracts)),
            'signed_contracts': list(map(Sendable.get_sendable_callback, self.signed_contracts)),
            'terminated_contracts': list(map(Sendable.get_sendable_callback, self.terminated_contracts)),
            'timestamp': self.timestamp,
            '_hash': self._hash
        }

    def from_json(self, json_str):
        self._hash = ""
