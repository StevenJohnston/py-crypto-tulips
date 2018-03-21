"""
Block Service Module
"""
from crypto_tulips.dal.services.redis_service import RedisService
from crypto_tulips.dal.services.block_service import BlockService as BlockServiceDal
from crypto_tulips.services.transaction_service import TransactionService
from crypto_tulips.services.contract_transaction_service import ContractTransactionService
from crypto_tulips.services.pos_transaction_service import PosTransactionService
from crypto_tulips.dal.objects.block import Block

import redis

class BlockService():
    """
    Block Service
    """

    @staticmethod
    def add_block_to_chain(block):
        """
        Method Comment
        """
        block_service_dal = BlockServiceDal()
        return block_service_dal.store_block(block)

    @staticmethod
    def get_max_height():
        """
        Method Comment
        """
        block_service_dal = BlockServiceDal()
        return block_service_dal.get_max_block_height()

    @staticmethod
    def verfiy_block(block):
        signature_valid = block.valid_signature()
        hash_valid = block.valid_hash()
        transactions_valid = BlockService.verify_transactions(block)
        return signature_valid and hash_valid and transactions_valid

    @staticmethod
    def remove_stale_blocks():
        """
        Removes stale, unused blocks.
        Blocks are removed if starting from the newest block, they do not appear when following the chain of previous blocks.
        ie.

        []<-[]<-[]<-[]<-[]<-[]<-[]<-[]<-[]<-[]
                    ^---[]<-[]<-[]<-[]<-[]

        In the above scenario, the bottom chain would be removed, moving all of those transactions back to the mempool.
        """
        block_dal = BlockServiceDal()
        current_height = block_dal.get_max_block_height()
        highest_blocks = block_dal.find_by_height(current_height)

        # if there is only 1 block at the greatest height, we can prune old blocks
        if len(highest_blocks) == 1:
            # get all block hashes
            all_block_hashes = block_dal.get_all_block_hashes()
            correct_block_hashes = set()
            block = highest_blocks[0]
            # add current highest block to the set of correct blocks
            correct_block_hashes.add(block._hash)
            # TODO while there is still a previous block
            while block.prev_block != 'GENESIS_BLOCK':
                block = block_dal.find_by_hash(block.prev_block)
                # add to list of correct blocks
                correct_block_hashes.add(block._hash)

            print("correct_block_hashes len: " + str(len(correct_block_hashes)))
            print("\t" + str(correct_block_hashes))
            # get the difference between the two sets of blocks
            to_remove = set(all_block_hashes) - correct_block_hashes
            print("to_remove: " + str(to_remove))
            # remove each of the blocks
            for block_hash in to_remove:
                print("Removing block: " + block_hash)
                BlockService._remove_block_by_hash(block_hash)

    @staticmethod
    def _remove_block_by_hash(block_hash):
        """
        Remove a block and restore it's transactions to the mempool.

        Parameters:
        block_hash  -- hash of block to remove
        """
        rs = RedisService()
        block_dal = BlockServiceDal()
        block = block_dal.find_by_hash(block_hash)

        # put all transaction types back into the mempool
        for transaction in block.transactions:
            TransactionService.add_to_mem_pool(transaction)
        for contract_transaction in block.contract_transactions:
            ContractTransactionService.add_to_mem_pool(contract_transaction)
        for pos_transaction in block.pos_transactions:
            PosTransactionService.add_to_mem_pool(pos_transaction)

        r = redis.StrictRedis()
        # remove from the sorted set of blocks
        r.zrem('blocks', block_hash)
        # remove from the set of blocks at it's height
        r.srem('block:' + str(block.height), block_hash)

        # delete the actual block
        rs.delete_by_key('block:' + block_hash)

    @staticmethod
    def get_last_block_hash():
        """
        Gets the highest block's hash.

        Returns:
        string  -- hash of the highest block
        """
        block_dal = BlockServiceDal()
        max_height = block_dal.get_max_block_height()
        latest_blocks = block_dal.find_by_height(max_height)
        if len(latest_blocks) != 0:
            return latest_blocks[0]._hash
        else:
            # TODO
            return 'GENESIS_BLOCK'

    @staticmethod
    def verify_transactions(new_block):
        block_service_dal = BlockServiceDal()
        transactions_before_block = block_service_dal.get_all_transaction_up_to_block(new_block.prev_block)

        duplicate_transaction = False
        signatures_valid = True
        hashes_valid = True
        # balance for each from_addr in new block
        balances = {}
        for block_transaction in new_block.transactions:
            # update address current balance
            balances[block_transaction.from_addr] = block_transaction.amount + balances.get(block_transaction.from_addr, 0)
            # check that the transaction isnt used in earlier block
            if block_transaction._hash not in transactions_before_block:
                duplicate_transaction = True
                # TODO add logger
            # signature validation
            if new_block.prev_block and not block_transaction.valid_signature():
                signatures_valid = False
            if not block_transaction.valid_hash():
                hashes_valid = False

        # update balances using all transaction from the past
        for key, transaction in transactions_before_block:
            if transaction.from_addr in balances:
                balances[transaction.from_addr] -= transaction.amount
            if transaction.to_addr in balances:
                balances[transaction.to_addr] += transaction.amount
        # not genesis block
        all_balance_positive = True
        if new_block.prev_block:
            # make sure each balance > 0
            for key, balance in balances:
                if balance < 0:
                    all_balance_positive = False
                    # TODO add logger
                    break
        return duplicate_transaction and all_balance_positive
