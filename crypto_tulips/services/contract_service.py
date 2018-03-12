"""
Contract Service
"""

import redis
import json
from crypto_tulips.dal.services.redis_service import RedisService
from crypto_tulips.services.base_object_service import BaseObjectService

class ContractService(BaseObjectService):
    """
    Contract Service Class
    """

    @staticmethod
    def get_contracts_from_public_key(public_key, include_mempool):
        """
        Get all regular contracts sent FROM a given public key

        Arguments:
        public_key      -- string of the public key to query the blockchain with
        include_mempool -- True if want results in the mempool as well, False otherwise

        Returns:
        list        -- list containing contracts from the given public key
        """
        return super(ContractService, ContractService).get_objects_from_public_key(public_key, include_mempool, Contract)

    @staticmethod
    def get_contracts_to_public_key(public_key, include_mempool):
        """
        Get all regular contracts sent TO a given public key

        Arguments:
        public_key      -- string of the public key to query the blockchain with
        include_mempool -- True if want results in the mempool as well, False otherwise

        Returns:
        list    -- list containing contracts to the given public key
        """
        return super(ContractService, ContractService).get_objects_to_public_key(public_key, include_mempool, Contract)

    @staticmethod
    def get_contracts_by_public_key(public_key, include_mempool):
        """
        Get all regular contracts (to and from) a given public key

        Arguments:
        public_key      -- string of the public key to query the blockchain with
        include_mempool -- True if want results in the mempool as well, False otherwise

        Returns:
        list        -- list containing all contracts that a given public key was a part of
            AND
        float       -- float containing current balance for the supplied public key
        """
        return super(ContractService, ContractService).get_objects_by_public_key(public_key, include_mempool, Contract)
        
