import json
import redis
from crypto_tulips.dal.objects.block import Block
from crypto_tulips.dal.objects.transaction import Transaction
from crypto_tulips.dal.objects.contract_transaction import ContractTransaction
from crypto_tulips.dal.objects.pos_transaction import PosTransaction
from crypto_tulips.dal.objects.terminated_contract import TerminatedContract

from crypto_tulips.logger.crypt_logger import Logger, LoggingLevel
from crypto_tulips.dal.services.redis_service import RedisService
from crypto_tulips.dal.services.contract_service import ContractService
from crypto_tulips.dal.services.signed_contract_service import SignedContractService

class BlockService():
    _host = ''
    _port = ''

    key_suffix = 'block:'
    max_block_height = 'max_block_height'

    rs = None
    def __init__(self):
        #settings = json.load(open('crypto_tulips/config/db_settings.json'))
        with open(file="crypto_tulips/config/db_settings.json", mode="r") as data_file:
            settings = json.load(data_file)
        self.host = settings["host"]
        self.port = settings["port"]
        #Logger.log("BlockService Initialized with redis running on " + self.host + ":" + self.port, 0, LoggingLevel.INFO)
        self.rs = RedisService()

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

        #rs = RedisService()

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
                transaction.is_mempool = 0
                # check if transaction is in the mempool
                set_name = transaction._to_index()[-1] + ":is_mempool:1"
                t_key = transaction._to_index()[-1] + ":" + transaction._hash
                if r.sismember(set_name, t_key):
                    # remove from list of mempool objects
                    pipe.srem(set_name, t_key)

                # store the transaction's hash under the block's list
                pipe.rpush(name, transaction._hash)
                # store the actual transaction object

                pipe = self.rs.store_object(transaction, r, pipe)

            pipe.rpush(name, 'pos_transactions')
            for pos_transaction in block.pos_transactions:
                pos_transaction.is_mempool = 0
                # check if pos transaction is in the mempool
                set_name = pos_transaction._to_index()[-1] + ":is_mempool:1"
                pt_key = pos_transaction._to_index()[-1] + ":" + pos_transaction._hash
                if r.sismember(set_name, pt_key):
                    # remove from list of mempool objects
                    pipe.srem(set_name, pt_key)

                pipe.rpush(name, pos_transaction._hash)
                pipe = self.rs.store_object(pos_transaction, r, pipe)

            pipe.rpush(name, 'contract_transactions')
            for contract_transaction in block.contract_transactions:
                contract_transaction.is_mempool = 0
                # check if contract transaction is in the mempool
                set_name = contract_transaction._to_index()[-1] + ":is_mempool:1"
                ct_key = contract_transaction._to_index()[-1] + ":" + contract_transaction._hash
                if r.sismember(set_name, ct_key):
                    # remove from list of mempool objects
                    pipe.srem(set_name, ct_key)

                pipe.rpush(name, contract_transaction._hash)
                pipe = self.rs.store_object(contract_transaction, r, pipe)

            pipe.rpush(name, 'contracts')
            for contract in block.contracts:
                contract.is_mempool = 0
                # check if contract is in the mempool
                set_name = contract._to_index()[-1] + ":is_mempool:1"
                c_key = contract._to_index()[-1] + ":" + contract._hash
                if r.sismember(set_name, c_key):
                    # remove from list of mempool objects
                    pipe.srem(set_name, c_key)

                pipe.rpush(name, contract._hash)
                pipe = ContractService.store_contract(contract, pipe)

            pipe.rpush(name, 'signed_contracts')
            for signed_contract in block.signed_contracts:
                signed_contract.is_mempool = 0
                # check if signed contract is in the mempool
                set_name = signed_contract._to_index()[-1] + ":is_mempool:1"
                sc_key = signed_contract._to_index()[-1] + ":" + signed_contract._hash
                if r.sismember(set_name, sc_key):
                    # remove from list of mempool objects
                    pipe.srem(set_name, sc_key)

                pipe.rpush(name, signed_contract._hash)
                pipe = SignedContractService.store_signed_contract(signed_contract, pipe)

            pipe.rpush(name, 'terminated_contracts')
            for terminated_contract in block.terminated_contracts:
                pipe.rpush(name, terminated_contract._hash)
                pipe = self.rs.store_object(terminated_contract, r, pipe)

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

        #rs = RedisService()

        # get key to retrieve list of block's fields
        name = self.key_suffix + block_hash

        if r.exists(name):
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
            contracts = []
            signed_contracts = []
            terminated_contracts = []

            # temporary list to copy from
            temp_list = []
            obj = None
            contract_section = False
            signed_contract_section = False
            terminated_contract_section = False
            for h in hashes:
                # if at a new type of object, change some variables
                if h == 'transactions':
                    prefix = Transaction._to_index()[-1]
                    obj = Transaction
                    continue
                elif h == 'pos_transactions':
                    prefix = PosTransaction._to_index()[-1]
                    obj = PosTransaction
                    transactions = temp_list.copy()
                    temp_list.clear()
                    continue
                elif h == 'contract_transactions':
                    prefix = ContractTransaction._to_index()[-1]
                    obj = ContractTransaction
                    pos_transactions = temp_list.copy()
                    temp_list.clear()
                    continue
                elif h == 'contracts':
                    contract_section = True
                elif h == 'signed_contracts':
                    contract_section = False
                    signed_contract_section = True
                elif h == 'terminated_contracts':
                    signed_contract_section = False
                    terminated_contract_section = True


                # get the object from redis and add to the temporary list
                if contract_section:
                    contract = ContractService.get_contract_by_hash(h)
                    if contract != None:
                        contracts.append(contract)
                elif signed_contract_section:
                    signed_contract = SignedContractService.get_signed_contract_by_hash(h)
                    if signed_contract != None:
                        signed_contracts.append(signed_contract)
                elif terminated_contract_section:
                    terminated_contract = self.rs.get_object_by_full_key('terminated_contract:' + h, TerminatedContract, r)
                    if terminated_contract != None:
                        terminated_contracts.append(terminated_contract)
                else:
                    t = self.rs.get_object_by_full_key(prefix + ":" + h, obj, r)
                    temp_list.append(t)

            contract_transactions = temp_list.copy()
            temp_list.clear()

            # create block object and return it
            block = Block(block_hash, signature, owner, prev_block, height, transactions, pos_transactions, contract_transactions, contracts, signed_contracts, terminated_contracts, timestamp)
            return block
        else:
            return None

    def get_max_block_height(self):
        """
        Gets the largest block height currently stored.

        Returns:
        int -- height of last block
        """
        r = self._connect()
        if not r.exists(self.max_block_height):
            r.set(self.max_block_height, 0)
        return int(r.get(self.max_block_height))

    def find_by_height(self, block_height):
        """
        Find a block using it's height. Will return the block object, fully populated with all of the objects encased in it.

        Arguments:
        block_height    -- height of the block to retrieve

        Returns:
        block object    -- Block object containing all of the objects included in the block
        """
        r = self._connect()
        hashes = r.smembers("block:" + str(block_height))
        blocks = list()
        for h in hashes:
            block = self.find_by_hash(h)
            blocks.append(block)
        return blocks

    def get_blocks_after_height(self, block_height):
        """
        Get all blocks chained after a given height.

        Arguments:
        block_height    -- Block height of block to retrieve all blocks after

        Returns:
        list    -- list containing all of the blocks in the chain after the supplied block height
        """
        max_height = self.get_max_block_height()
        blocks = list()
        # want blocks between current and the max height
        if int(max_height) > int(block_height):
            # get blocks by height for heights between the supplied and max
            for height in range(int(block_height), int(max_height) + 1):
                new_blocks = self.find_by_height(height)
                blocks.extend(new_blocks)
        return blocks

    def get_blocks_after_hash(self, block_hash):
        """
        Get all blocks chained after a given hash.

        Arguments:
        block_hash  -- Block hash of block to retrieve all blocks after

        Returns:
        list    -- list containing all of the blocks in the chain after the supplied block hash
        """
        current_block = self.find_by_hash(block_hash)
        return self.get_blocks_after_height(current_block.height)

    def get_all_block_hashes(self):
        """
        Get all block hashes.

        Returns:
        list    -- list of strings containing all block hashes
        """
        r = self._connect()
        block_hashes = r.zrange('blocks', 0, -1)
        return block_hashes

    def _connect(self):
        # charset and decode_responses will need to be removed if we want this to be actually stored
        # as bytes (per: https://stackoverflow.com/questions/25745053/about-char-b-prefix-in-python3-4-1-client-connect-to-redis)
        return redis.StrictRedis(self.host, self.port, db=0, charset="utf-8", decode_responses="True")

    def get_all_transaction_up_to_block(self, block_hash):
        block = self.find_by_hash(block_hash)
        if block:
            transactions = block.transactions
            while block.prev_block:
                block = self.find_by_hash(block.prev_block)
                transactions.extend(block.transactions)
            return {transaction._hash: transaction for transaction in transactions}
        else:
            return {}

    def get_all_pos_transaction(self, block_hash):
        block = self.find_by_hash(block_hash)
        if block:
            pos_transactions = block.pos_transactions
            while block.prev_block:
                block = self.find_by_hash(block.prev_block)
                pos_transactions.extend(block.pos_transactions)
            return {pos_transaction._hash: pos_transaction for pos_transaction in pos_transactions}


    def get_all_objects_up_to_block(self, block):
        if block:
            transactions = block.transactions.copy()
            pos_transactions = block.pos_transactions.copy()
            contract_transactions = block.contract_transactions.copy()
            contracts = block.contracts.copy()
            signed_contracts = block.signed_contracts.copy()
            terminated_contracts = block.terminated_contracts.copy()
            owners = [block.owner]

            while block.prev_block:
                block = self.find_by_hash(block.prev_block)
                transactions.extend(block.transactions)
                pos_transactions.extend(block.pos_transactions)
                contract_transactions.extend(block.contract_transactions)
                contracts.extend(block.contracts)
                signed_contracts.extend(block.signed_contracts)
                terminated_contracts.extend(block.terminated_contracts)
                owners.append(block.owner)
            # convert to dictionaries
            transaction_dict = {transaction._hash: transaction for transaction in transactions}
            pos_transaction_dict = {pos_transaction._hash: pos_transaction for pos_transaction in pos_transactions}
            contract_transaction_dict = {contract_transaction._hash: contract_transaction for contract_transaction in contract_transactions}
            contract_dict = {contract._hash: contract for contract in contracts}
            signed_contract_dict = {signed_contract._hash: signed_contract for signed_contract in signed_contracts}
            terminated_contract_dict = {terminated_contract._hash: terminated_contract for terminated_contract in terminated_contracts}
            return {'transactions': transaction_dict, 'pos_transactions': pos_transaction_dict, 'contract_transactions': contract_transaction_dict, 'contracts': contract_dict, 'signed_contracts': signed_contract_dict, 'terminated_contracts': terminated_contract_dict, 'owners': owners}
        else:
            return {}
