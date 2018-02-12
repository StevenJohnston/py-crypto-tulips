import redis
import json

# Stored in database with key -> value
#       block:id:actual_hash_here -> block_data

class Block:
    __block_hash = ''
    __block_data = ''
    __host = ''
    __port = ''

    key_format =  'block:{}:{}'

    id_store_key = 'block:current_id'

    def __init__(self, block_hash, block_data):
        self.block_hash = block_hash
        self.block_data = block_data
        settings = json.load(open('db_settings.json'))
        self.host = settings[0]["host"]
        self.port = settings[0]["port"]

    def store_block(self):
        r = redis.StrictRedis(host='localhost', port=6379, db=0)

        if r.exists(Block.id_store_key):
            # get and increment id
            next_id = r.incr(Block.id_store_key)
        else:
            # if id isn't set yet (no blocks), start at 1
            next_id = r.set(Block.id_store_key, 1)

        r.set(Block.key_format.format(next_id, self.block_hash), self.block_data)

    def check_next_block_id(self):
        r = redis.Redis(self.host, self.port, db=0)
        return r.get(Block.id_store_key)