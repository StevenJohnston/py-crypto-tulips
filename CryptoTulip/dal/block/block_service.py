import json
import redis
import block

class BlockService:
    __host = ''
    __port = ''

    id_store_key = 'block:current_id'

    def __init__(self):
        settings = json.load(open('db_settings.json'))
        self.host = settings[0]["host"]
        self.port = settings[0]["port"]

    def store_block(self, block):
        r = self.__connect()
        return r.set(block.block_hash, block.block_data)

    def check_next_block_id(self, block):
        r = self.__connect()
        return r.get(BlockService.id_store_key)

    def find_by_hash(self, block_hash):
        r = self.__connect()
        return r.get(block_hash)

    def __connect(self):
        return redis.Redis(BlockService.__host, BlockService.__port, db=0)
