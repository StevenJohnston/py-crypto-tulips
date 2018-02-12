# Stored in database with keys:
#       block:id:hash 
#   and 
#       block:id:data

class Block:
    __block_hash = '' 
    __block_data = ''


    def __init__(self, block_hash, block_data):
        self.block_hash = block_hash
        self.block_data = block_data
