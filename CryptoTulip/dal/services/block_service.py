import json
import redis
from objects import block

class BlockService:
    __host = ''
    __port = 3000

    id_store_key = 'block:current_id'
    key_format = 'block:{}'

    def __init__(self):
        settings = json.load(open('db_settings.json'))
        print(settings["host"] + ":" + settings["port"])
        self.host = settings["host"]
        self.port = settings["port"]

    def store_block(self, block):
        r = self.__connect()
        return r.set(block.block_hash, block.block_data)

    def check_next_block_id(self, block):
        r = self.__connect()
        return r.get(BlockService.id_store_key)

    def find_by_hash(self, block_hash):
        r = self.__connect()

        block_data = r.get(block_hash)
        b = block.Block(block_hash, block_data)
        print("newblock=" + b.to_string())
        return b

    def __connect(self):
        return redis.Redis(self.host, self.port, db=0)
