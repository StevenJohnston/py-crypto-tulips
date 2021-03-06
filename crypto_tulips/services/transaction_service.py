"""
Transaction Service Module
"""

from crypto_tulips.dal.objects.transaction import Transaction
from crypto_tulips.services.base_object_service import BaseObjectService

class TransactionService(BaseObjectService):
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
    def ensure_enough_funds(new_transaction):
        """
        Checks a public key's TO and FROM transactions to ensure that they have enough balance remaining to create the new transaction.

        Arguments:
        new_transaction -- transaction object of the new transaction that is trying to be made

        Returns:
        boolean -- True if enough funds are present, False if not
        """
        public_key = new_transaction.from_addr
        amount = new_transaction.amount
        transactions, balance = TransactionService.get_transactions_by_public_key(public_key, False)
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
        return super(TransactionService, TransactionService).get_objects_from_public_key(public_key, include_mempool, Transaction)

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
        return super(TransactionService, TransactionService).get_objects_to_public_key(public_key, include_mempool, Transaction)

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
        return super(TransactionService, TransactionService).get_objects_by_public_key(public_key, include_mempool, Transaction)

    @staticmethod
    def get_all_mempool_transactions():
        return super(TransactionService, TransactionService).get_all_mempool_objects(Transaction)

    @staticmethod
    def get_10_transactions_from_mem_pool():
        return super(TransactionService, TransactionService).get_from_mem_pool(Transaction)
