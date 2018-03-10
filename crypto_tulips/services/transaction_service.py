"""
Transaction Service Module
"""

from crypto_tulips.dal.objects.transaction import Transaction
from crypto_tulips.services.base_transaction_service import BaseTransactionService

class TransactionService(BaseTransactionService):
    """
    Transaction Service
    """

    @staticmethod
    def create_new_transaction():
        """
        Method Comment
        """
        pass

    @staticmethod
    def verfiy_rsa():
        """
        Method Comment
        """
        pass

    @staticmethod
    def verify_ownership_of_funds(new_transaction):
        """
        """
        public_key = new_transaction.from_addr
        amount = new_transaction.amount
        transactions, balance = TransactionService.get_transactions_by_public_key(public_key, True)
        if (balance >= amount):
            # address has enough funds for the new transaction
            return True
        else:
            # address does not have enough funds
            return False



    @staticmethod
    def get_transactions_from_public_key(public_key, include_mempool):
        """
        Get all regular transactions sent FROM a given public key

        Arguments:
        public_key      -- string of the public key to query the blockchain with
        include_mempool -- True if want results in the mempool as well, False otherwise

        Returns:
        list        -- list containing transactions from the given public key
        """
        return super(TransactionService, TransactionService).get_transactions_from_public_key(public_key, include_mempool, Transaction)

    @staticmethod
    def get_transactions_to_public_key(public_key, include_mempool):
        """
        Get all regular transactions sent TO a given public key

        Arguments:
        public_key      -- string of the public key to query the blockchain with
        include_mempool -- True if want results in the mempool as well, False otherwise

        Returns:
        list    -- list containing transactions to the given public key
        """
        return super(TransactionService, TransactionService).get_transactions_to_public_key(public_key, include_mempool, Transaction)

    @staticmethod
    def get_transactions_by_public_key(public_key, include_mempool):
        """
        Get all regular transactions (to and from) a given public key

        Arguments:
        public_key      -- string of the public key to query the blockchain with
        include_mempool -- True if want results in the mempool as well, False otherwise

        Returns:
        list        -- list containing all transactions that a given public key was a part of
            AND
        float       -- float containing current balance for the supplied public key
        """
        return super(TransactionService, TransactionService).get_transactions_by_public_key(public_key, include_mempool, Transaction)

    @staticmethod
    def get_10_transactions_from_mem_pool():
        return super(TransactionService, TransactionService).get_from_mem_pool(Transaction)
