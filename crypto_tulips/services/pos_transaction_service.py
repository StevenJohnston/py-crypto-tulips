"""
Pos Transaction Service Module
"""

from crypto_tulips.dal.objects.pos_transaction import PosTransaction
from crypto_tulips.services.base_transaction_service import BaseTransactionService

class PosTransactionService(BaseTransactionService):
    """
    Pos Transaction Service
    """

    @staticmethod
    def get_pos_transactions_from_public_key(public_key):
        return super(PosTransactionService, PosTransactionService).get_transactions_from_public_key(public_key, PosTransaction)

    @staticmethod
    def get_10_pos_transactions_from_mem_pool():
        return super(PosTransactionService, PosTransactionService).get_from_mem_pool(PosTransaction)