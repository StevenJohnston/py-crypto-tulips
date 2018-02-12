import redis

# Stored in database with key -> value
#       block:id:actual_hash_here -> block_data

class Block:
    __block_hash = '' 
    __block_data = ''

    key_format =  'block:{}:{}'

    id_store_key = 'block:current_id'

    def __init__(self, block_hash, block_data):
        self.block_hash = block_hash
        self.block_data = block_data


    def store_block(self):
        r = redis.StrictRedis(host='localhost', port=6379, db=0)
        r.get(Block.id_store_key)
        r.set(Block.key_format.format(id, self.block_hash), self.block_data)
