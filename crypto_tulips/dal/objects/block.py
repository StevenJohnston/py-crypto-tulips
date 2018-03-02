# Stored in database with key -> value
#       block:id:actual_hash_here -> block_data

class Block:
    block_hash = ''
    block_data = ''

    prefix = 'block'

    transactions = []

    def __init__(self, block_hash, block_data, transactions):
        self.block_hash = block_hash
        self.block_data = block_data
        self.transactions = transactions

    def to_string(self):
        return str(self.block_hash) + "->" + str(self.block_data)

    def from_json(self, json_str):
        self.block_hash = ""
