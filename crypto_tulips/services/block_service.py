"""
Block Service Module
"""
from crypto_tulips.dal.services.block_service import BlockService as BlockServiceDal
from crypto_tulips.services.transaction_service import TransactionService
from crypto_tulips.dal.objects.block import Block

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
