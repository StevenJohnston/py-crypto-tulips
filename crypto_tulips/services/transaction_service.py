"""
Transaction Service Module
"""

from dal.objects.transaction import Transaction
from services.base_transaction_service import BaseTransactionService

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
    def verify_ownership_of_funds():
        """
        Method Comment
        """
        pass

    @staticmethod
    def get_transactions_from_public_key(public_key):
        return super(TransactionService, TransactionService).get_transactions_from_public_key(public_key, Transaction)

    @staticmethod
    def get_transactions_to_public_key(public_key):
        return super(TransactionService, TransactionService).get_transactions_to_public_key(public_key, Transaction)

    @staticmethod
    def get_transactions_by_public_key(public_key):
        return super(TransactionService, TransactionService).get_transactions_by_public_key(public_key, Transaction)