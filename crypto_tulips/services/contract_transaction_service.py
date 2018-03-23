"""
Contract Transaction Service Module
"""

from crypto_tulips.dal.objects.contract_transaction import ContractTransaction
from crypto_tulips.services.base_object_service import BaseObjectService
from crypto_tulips.dal.services.redis_service import RedisService

import redis

class ContractTransactionService(BaseObjectService):
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
        return super(ContractTransactionService, ContractTransactionService).get_objects_from_public_key(public_key, include_mempool, ContractTransaction)

    @staticmethod
    def get_contract_transactions_for_contract_address(contract_address, include_mempool):
        """
        Get all contract transactions by a given contract address.

        Arguments:
        contract_address    -- public key of contract
        include_mempool     -- True if want results in the mempool, False otherwise

        Returns:
        list    -- list containing contract transactions made on the contract address
        """
        rs = RedisService()
        r = rs._connect()
        address_set = 'contract_transaction:contract_addr:' + contract_address
        mempool_set = 'contract_transaction:is_mempool:1'

        contract_t_keys = list()
        if include_mempool:
            contract_t_keys = r.smembers(address_set)
        else:
            contract_t_keys = r.sdiff(address_set, mempool_set)

        contract_transactions = list()
        for contract_t_key in contract_t_keys:
            ct = rs.get_object_by_full_key(contract_t_key, ContractTransaction)
            contract_transactions.append(ct)
        return contract_transactions

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