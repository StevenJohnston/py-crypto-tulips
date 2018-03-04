from crypto_tulips.dal.objects.block import Block
from crypto_tulips.dal.objects.transaction import Transaction
from crypto_tulips.dal.objects.pos_transaction import PosTransaction
from crypto_tulips.hashing.crypt_hashing import Hashing
import time
class GenesisBlockService():
    @staticmethod
    def generate_from_priv(private_key):
        public = Hashing.get_public_key(private_key)
        transcations = [
            new Transaction('', '', public, '', 1, time.time()),
            new Transaction('', '', public, '', 10, time.time()),
            new Transaction('', '', public, '', 100, time.time()),
            new Transaction('', '', public, '', 1000, time.time()),
        ]
        for tranaction in transcations:
            tranaction.update_signature(private_key)
            tranaction.update_hash()

        pos_transactions = [
                new PosTransaction('', '',public, 100, time.time())
            ]

        for pos_transaction in pos_transactions:
            pos_transaction.update_signature(private_key)
            pos_transaction.update_hash()
            
        
        block = new Block('', '',transactions, pos_transactions)
        block.update_signature(private_key)
        block.update_hash()
        return block

        @staticmethod
    def generate_from_file():
        data = json.load(open('crypto_tulips/config/genesis_block.json'))
        with open('crypto_tulips/config/genesis_block.json', 'r') as myfile:
            private_key = myfile.read()
        public = Hashing.get_public_key(private_key)
        block = new Block('', '',transactions, pos_transactions)
        block.update_hash()
        return block


        