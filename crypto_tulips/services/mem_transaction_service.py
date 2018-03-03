"""
MemTransaction Service Module
"""

from dal.objects.mem_transaction import MemTransaction
from services.base_transaction_service import BaseTransactionService

class MemTransactionService(BaseTransactionService):
    """
    Mempool Transaction Service
    """

    @staticmethod
    def get_transactions_from_public_key(public_key):
        return super(MemTransactionService, MemTransactionService).get_transactions_from_public_key(public_key, MemTransaction)

    @staticmethod
    def get_transactions_to_public_key(public_key):
        return super(MemTransactionService, MemTransactionService).get_transactions_to_public_key(public_key, MemTransaction)

    @staticmethod
    def get_transactions_by_public_key(public_key):
        return super(MemTransactionService, MemTransactionService).get_transactions_by_public_key(public_key, MemTransaction)