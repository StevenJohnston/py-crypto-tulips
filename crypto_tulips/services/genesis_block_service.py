from crypto_tulips.dal.objects.block import Block
from crypto_tulips.hashing.crypt_hashing import Hashing

class GenesisBlockService():
    def __init__(self):
    
    @staticmethod
    def generate_from_priv(private_key, transactions, pos_transactions):
        # get public key
        # public = Hashing.generate_rsa_key()
        block = new Block('', transactions, pos_transactions)
        