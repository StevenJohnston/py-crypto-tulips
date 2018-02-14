# Stored in database with key -> value
#       block:actual_hash_here -> block_data

class Block:
    __block_hash = ''
    __block_data = ''

    def __init__(self, block_hash, block_data):
        self.block_hash = block_hash
        self.block_data = block_data

    def to_string(self):
        return str(self.block_hash) + "|" + str(self.block_data)