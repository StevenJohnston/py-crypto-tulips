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
    def get_contract_transactions_from_public_key(public_key):
        return super(ContractTransactionService, ContractTransactionService).get_transactions_from_public_key(public_key, ContractTransaction)

    @staticmethod
    def get_contract_transactions_to_public_key(public_key):
        return super(ContractTransactionService, ContractTransactionService).get_transactions_to_public_key(public_key, ContractTransaction)

    @staticmethod
    def get_contract_transactions_by_public_key(public_key):
        return super(ContractTransactionService, ContractTransactionService).get_transactions_by_public_key(public_key, ContractTransaction)

    @staticmethod
    def get_10_contract_transactions_from_mem_pool():
        return super(ContractTransactionService, ContractTransactionService).get_from_mem_pool(ContractTransaction)