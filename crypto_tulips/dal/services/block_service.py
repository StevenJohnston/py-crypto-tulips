import json
import redis
from dal.objects import block
from logger import crypt_logger

class BlockService:
    _host = ''
    _port = 3000

    key_suffix = 'block:'

    def __init__(self):
        settings = json.load(open('config/db_settings.json'))
        self.host = settings["host"]
        self.port = settings["port"]
        crypt_logger.Logger.log("BlockService Initialized with redis running on " + self.host + ":" + self.port, 0, crypt_logger.LoggingLevel.INFO)

    def store_block(self, block):
        r = self._connect()
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