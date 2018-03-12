"""
Pos Transaction Service Module
"""

from crypto_tulips.dal.objects.pos_transaction import PosTransaction
from crypto_tulips.services.base_object_service import BaseObjectService

class PosTransactionService(BaseObjectService):
    """
    Pos Transaction Service
    """

    @staticmethod
    def get_pos_transactions_from_public_key(public_key, include_mempool = True):
        """
        Get all proof of stake transactions sent FROM a given public key

        Arguments:
        public_key      -- string of the public key to query the blockchain with
        include_mempool -- True if want results in the mempool as well, False otherwise

        Returns:
        list        -- list containing transactions from the given public key
        """
        return super(PosTransactionService, PosTransactionService).get_transactions_from_public_key(public_key, include_mempool, PosTransaction)

    @staticmethod
    def get_10_pos_transactions_from_mem_pool():
        return super(PosTransactionService, PosTransactionService).get_from_mem_pool(PosTransaction)