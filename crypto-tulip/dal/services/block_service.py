import json
import redis
from objects import block

class BlockService:
    _host = ''
    _port = 3000

    key_suffix = 'block:'

    def __init__(self):
        settings = json.load(open('db_settings.json'))
        print(settings["host"] + ":" + settings["port"])
        self.host = settings["host"]
        self.port = settings["port"]

    def store_block(self, block):
        r = self._connect()
        #print("full key: " + BlockService.key_suffix + block.block_hash)
        return r.set(BlockService.key_suffix + block.block_hash, block.block_data)

    def find_by_hash(self, block_hash):
        r = self._connect()
        block_data = r.get(BlockService.key_suffix + block_hash)
        b = block.Block(block_hash, block_data)
        return b

    def get_all_blocks(self):
        r = self._connect()

    def _connect(self):
        # charset and decode_responses will need to be removed if we want this to be actually stored
        # as bytes (per: https://stackoverflow.com/questions/25745053/about-char-b-prefix-in-python3-4-1-client-connect-to-redis)
        return redis.StrictRedis(self.host, self.port, db=0, charset="utf-8", decode_responses="True")
