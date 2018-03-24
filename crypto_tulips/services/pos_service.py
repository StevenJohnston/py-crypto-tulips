"""
Block Service Module
"""
from crypto_tulips.dal.services.redis_service import RedisService
from crypto_tulips.dal.services.block_service import BlockService as BlockServiceDal
from crypto_tulips.services.transaction_service import TransactionService
from crypto_tulips.services.contract_transaction_service import ContractTransactionService
from crypto_tulips.services.pos_transaction_service import PosTransactionService
from crypto_tulips.dal.objects.block import Block

import redis

class POSService():
    
    @staticmethod
    def get_pos_pool(current_block):
      block_service_dal = BlockServiceDal()
      pos_transactions_before_block = block_service_dal.get_all_pos_transaction(current_block._hash)

      balances = {}
      # balances of all pos'ers
      for key, pos_transaction in pos_transactions_before_block.items():
          # update address current balance
          balances[pos_transaction.from_addr] = pos_transaction.amount + balances.get(pos_transaction.from_addr, 0)
          if balances[pos_transaction.from_addr] == 0:
            balances.pop(pos_transaction.from_addr, None)

      return balances
        
    @staticmethod
    def get_next_block_author(current_block):
      pos_pool = POSService.get_pos_pool(current_block)
      number_of_pos_accounts = len(pos_pool)
      pos_index = int(current_block._hash, 16) % number_of_pos_accounts
      ordered = sorted(list(pos_pool.keys()))

      return ordered[pos_index]
