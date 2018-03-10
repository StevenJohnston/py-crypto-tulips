"""
Contract Transaction Service Module
"""

from crypto_tulips.dal.objects.contract_transaction import ContractTransaction
from crypto_tulips.services.base_transaction_service import BaseTransactionService

class ContractTransactionService(BaseTransactionService):
    """
    Contract Transaction Service
    """

    @staticmethod
    def get_contract_transactions_from_public_key(public_key, include_mempool):
        """
        Get all contract transactions sent FROM a given public key

        Arguments:
        public_key      -- string of the public key to query the blockchain with
        include_mempool -- True if want results in the mempool as well, False otherwise

        Returns:
        list    -- list containing transactions from the given public key
        """
        return super(ContractTransactionService, ContractTransactionService).get_transactions_from_public_key(public_key, include_mempool, ContractTransaction)

    @staticmethod
    def get_contract_transactions_to_public_key(public_key, include_mempool):
        """
        Get all contract transactions sent TO a given public key

        Arguments:
        public_key      -- string of the public key to query the blockchain with
        include_mempool -- True if want results in the mempool as well, False otherwise

        Returns:
        list    -- list containing transactions to the given public key
        """
        return super(ContractTransactionService, ContractTransactionService).get_transactions_to_public_key(public_key, include_mempool, ContractTransaction)

    @staticmethod
    def get_contract_transactions_by_public_key(public_key, include_mempool):
        """
        Get all contract transactions (to and from) a given public key

        Arguments:
        public_key      -- string of the public key to query the blockchain with
        include_mempool -- True if want results in the mempool as well, False otherwise

        Returns:
        list        -- list containing all transactions that a given public key was a part of
            AND
        float       -- float containing current balance for the supplied public key
        """
        return super(ContractTransactionService, ContractTransactionService).get_transactions_by_public_key(public_key, include_mempool, ContractTransaction)

    @staticmethod
    def get_10_contract_transactions_from_mem_pool():
        """
        Get all transactions sent TO a given public key

        Arguments:
        public_key      -- string of the public key to query the blockchain with
        include_mempool -- True if want results in the mempool as well, False otherwise
        obj             -- either a Transaction or a MemTransaction empty object (doesn't need to be instantiated)
        redis_conn      -- redis connection if already established
        pipe            -- pipeline if already established
        rs              -- RedisService instance if established

        Returns:
        list        -- list containing transactions to the given public key
        """
        return super(ContractTransactionService, ContractTransactionService).get_from_mem_pool(ContractTransaction)