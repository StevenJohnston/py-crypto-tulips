"""
Contract Service
"""

import redis
import json
from crypto_tulips.dal.services.redis_service import RedisService

from crypto_tulips.dal.objects.contract import Contract
from crypto_tulips.dal.objects.signed_contract import SignedContract
from crypto_tulips.dal.objects.contract_transaction import ContractTransaction

from crypto_tulips.dal.services.contract_service import ContractFilter, ContractService as ContractServiceDal
from crypto_tulips.dal.services.signed_contract_service import SignedContractFilter, SignedContractService

from crypto_tulips.services.transaction_service import TransactionService

class ContractService:
    """
    Contract Service Class
    """

    @staticmethod
    def accept_signed_contract(signed_contract):
        base_contract = ContractServiceDal.get_contract_by_hash(signed_contract.parent_hash)
        if base_contract.is_mempool == 0 and \
            base_contract.sign_end_timestamp >= signed_contract.signed_timestamp:
        pass



