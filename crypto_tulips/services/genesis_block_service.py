from crypto_tulips.dal.objects.block import Block
from crypto_tulips.dal.objects.transaction import Transaction
from crypto_tulips.dal.objects.pos_transaction import PosTransaction
from crypto_tulips.hashing.crypt_hashing import Hashing
import time
import json
class GenesisBlockService():
    @staticmethod
    def generate_from_priv(private_key):
        time_now = 1520135639.4713802
        public = Hashing.get_public_key(private_key)
        transcations = [
            Transaction('', '', public, '', 1, time_now),
            Transaction('', '', public, '', 10, time_now),
            Transaction('', '', public, '', 100, time_now),
            Transaction('', '', public, '', 1000, time_now),
        ]

        for tranaction in transcations:
            tranaction.update_signature(private_key)
            tranaction.update_hash()

        pos_transactions = [
                PosTransaction('', '',public, 100, time_now)
            ]

        for pos_transaction in pos_transactions:
            pos_transaction.update_signature(private_key)
            pos_transaction.update_hash()
            
        
        block = Block('', '', transcations, pos_transactions, [], time_now)
        block.update_signature(private_key)
        block.update_hash()
        return block

    @staticmethod
    def generate_from_file():
        # data = json.load(open('crypto_tulips/config/genesis_block.json'))
        with open('crypto_tulips/config/genesis_block.json', 'r') as myfile:
            private_key = myfile.read()
        block = GenesisBlockService.generate_from_priv(private_key)
        return block


        