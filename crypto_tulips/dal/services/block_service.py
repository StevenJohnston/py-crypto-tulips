import json
import redis
from crypto_tulips.dal.objects.block import Block
from crypto_tulips.dal.objects.transaction import Transaction

from crypto_tulips.logger.crypt_logger import Logger, LoggingLevel
from crypto_tulips.dal.services.redis_service import RedisService

class BlockService:
    _host = ''
    _port = ''

    key_suffix = 'block:'
    max_block_height = 'max_block_height'

    def __init__(self):
        settings = json.load(open('crypto_tulips/config/db_settings.json'))
        self.host = settings["host"]
        self.port = settings["port"]
        Logger.log("BlockService Initialized with redis running on " + self.host + ":" + self.port, 0, LoggingLevel.INFO)

    def store_block(self, block):
        """
        Store an entire block in redis. Will store fields and lists of objects. Will not store anything if the block's hash already exists in the database.

        Arguments:
        block   -- Block object to be stored

        Returns:
        list    -- list containing results of each query used to store an object (0s and 1s)
                0s indicate that the field was updated (already present)
                1s indicate that the field is new and was stored
        """
        r = self._connect()

        rs = RedisService()

        # key to store list of objects under
        name = self.key_suffix + block._hash
        # if block isn't in the database already
        if not r.exists(name):
            pipe = r.pipeline()
            # store timestamp first
            pipe.rpush(name, block.prev_block)
            pipe.rpush(name, block.height)
            pipe.rpush(name, block.owner)
            pipe.rpush(name, block.signature)
            pipe.rpush(name, block.timestamp)

            # store string 'transactions' to help with retrieval parsing
            pipe.rpush(name, 'transactions')
            for transaction in block.transactions:
                # store the transaction's hash under the block's list
                pipe.rpush(name, transaction._hash)
                # store the actual transaction object
                rs.store_object(transaction, r, pipe)

            pipe.rpush(name, 'pos_transactions')
            for pos_transaction in block.pos_transactions:
                pipe.rpush(name, pos_transaction._hash)
                rs.store_object(pos_transaction, r, pipe)

            pipe.rpush(name, 'contract_transactions')
            for contract_transaction in block.contract_transactions:
                pipe.rpush(name, contract_transaction._hash)
                rs.store_object(contract_transaction, r, pipe)

            pipe.zadd('blocks', block.height, block._hash)

            # TODO max block height will not always be this, will change
            pipe.set(self.max_block_height, block.height)

            pipe.sadd("block:" + str(block.height), block._hash)
            return pipe.execute()
        else:
            print("Block with hash: " + block._hash + " already exists. Unable to update.")
            return []

    def find_by_hash(self, block_hash):
        """
        Find a block using it's hash. Will return the block object, fully populated with all of the objects encased in it.

        Arguments:
        block_hash      -- hash of the block to retrieve

        Returns:
        block object    -- Block object containing all of the objects included in the block
        """
        r = self._connect()

        rs = RedisService()

        # get key to retrieve list of block's fields
        name = self.key_suffix + block_hash

        # get all of the fields in the list
        hashes = r.lrange(name, 0, -1)

        # timestamp will always be first
        prev_block = hashes[0]
        # remove for iteration
        hashes.remove(prev_block)

        # timestamp will always be first
        height = hashes[0]
        # remove for iteration
        hashes.remove(height)

        # timestamp will always be first
        owner = hashes[0]
        # remove for iteration
        hashes.remove(owner)

        # timestamp will always be first
        signature = hashes[0]
        # remove for iteration
        hashes.remove(signature)

        # timestamp will always be first
        timestamp = hashes[0]
        # remove for iteration
        hashes.remove(timestamp)

        prefix = ''
        # list to hold all of the objects
        transactions = []
        pos_transactions = []
        contract_transactions = []

        # temporary list to copy from
        temp_list = []
        obj = None
        for h in hashes:
            # if at a new type of object, change some variables
            if h == 'transactions':
                prefix = Transaction._to_index()[-1]
                obj = Transaction
                continue
            elif h == 'pos_transactions':
                prefix = ''
                obj = Transaction
                transactions = temp_list.copy()
                temp_list.clear()
                # TODO class hasn't been created yet
                continue
            elif h == 'contract_transactions':
                prefix = ''
                obj = Transaction
                pos_transactions = temp_list.copy()
                temp_list.clear()
                # TODO class hasn't been created yet
                continue

            # get the object from redis and add to the temporary list
            t = rs.get_object_by_full_key(prefix + ":" + h, obj, r)
            temp_list.append(t)

        contract_transactions = temp_list.copy()
        temp_list.clear()

        # create block object and return it
        block = Block(block_hash, signature, owner, prev_block, height, transactions, pos_transactions, contract_transactions, timestamp)
        return block

    def get_max_block_height(self):
        r = self._connect()
        if not r.exists(self.max_block_height):
            r.set(self.max_block_height, 0)
        return r.get(self.max_block_height)

    def find_by_height(self, block_height):
        r = self._connect()
        hashes = r.smembers("block:" + str(block_height))
        blocks = list()
        for h in hashes:
            block = self.find_by_hash(h)
            blocks.append(block)
        return blocks

    def get_blocks_after_height(self, block_height):
        max_height = self.get_max_block_height()
        blocks = list()
        if int(max_height) > int(block_height):
            for height in range(int(block_height) + 1, int(max_height) + 1):
                new_blocks = self.find_by_height(height)
                blocks.extend(new_blocks)
        return blocks

    def get_blocks_after_hash(self, block_hash):
        current_block = self.find_by_hash(block_hash)
        return self.get_blocks_after_height(current_block.height)

    def _connect(self):
        # charset and decode_responses will need to be removed if we want this to be actually stored
        # as bytes (per: https://stackoverflow.com/questions/25745053/about-char-b-prefix-in-python3-4-1-client-connect-to-redis)
        return redis.StrictRedis(self.host, self.port, db=0, charset="utf-8", decode_responses="True")
