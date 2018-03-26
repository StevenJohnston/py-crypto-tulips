import redis
import time

from crypto_tulips.services.block_service import BlockService
from crypto_tulips.services.base_object_service import BaseObjectService

from crypto_tulips.dal.services.redis_service import RedisService
from crypto_tulips.dal.services.block_service import BlockService as BlockServiceDal
from crypto_tulips.dal.services.signed_contract_service import SignedContractService
from crypto_tulips.dal.services.contract_service import ContractService

from crypto_tulips.dal.objects.price_stamp import PriceStamp

from crypto_tulips.dal.objects.block import Block

from crypto_tulips.dal.objects.transaction import Transaction
from crypto_tulips.dal.objects.pos_transaction import PosTransaction
from crypto_tulips.dal.objects.contract_transaction import ContractTransaction
from crypto_tulips.dal.objects.contract import Contract
from crypto_tulips.dal.objects.signed_contract import SignedContract
from crypto_tulips.dal.objects.terminated_contract import TerminatedContract

from crypto_tulips.hashing.crypt_hashing_wif import EcdsaHashing
class Miner():
    @staticmethod
    def mine_block(miner_priv_key, last_block):
        balances = BlockService.get_all_balances()

        transactions = BaseObjectService.get_all_mempool_objects(Transaction)
        transactions_to_add = []
        for transaction in transactions:
            if len(transactions_to_add) == 10:
                break
            valid, balances = Miner.validate_transaction(balances, transaction)
            if valid:
                transactions_to_add.append(transaction)

        pos_transactions = BaseObjectService.get_all_mempool_objects(PosTransaction)
        pos_transactions_to_add = []
        for pos_transaction in pos_transactions:
            if len(pos_transactions_to_add) == 10:
                break
            valid, balances = Miner.validate_pos_transaction(balances, pos_transaction)
            if valid:
                pos_transactions_to_add.append(pos_transaction)

        contract_transactions = BaseObjectService.get_all_mempool_objects(ContractTransaction)
        contract_transactions_to_add = []
        for contract_transaction in contract_transactions:
            if len(contract_transactions_to_add) == 10:
                break
            valid, balances = Miner.validate_contract_transaction(balances, contract_transaction)
            if valid:
                contract_transactions_to_add.append(contract_transaction)

        contracts = BaseObjectService.get_all_mempool_objects(Contract)
        contracts_to_add = []
        for contract in contracts:
            if len(contracts_to_add) == 10:
                break
            valid, balances = Miner.validate_contract(balances, contract)
            if valid:
                contracts_to_add.append(contract)

        signed_contracts = BaseObjectService.get_all_mempool_objects(SignedContract)
        signed_contracts_to_add = []
        for signed_contract in signed_contracts:
            print('signed_contract:' + signed_contract._hash)
            if len(signed_contracts_to_add) == 10:
                break
            valid, balances = Miner.validate_signed_contract(balances, signed_contract)
            if valid:
                signed_contracts_to_add.append(signed_contract)

        terminated_contracts_to_add = []
        signed_contracts_to_check = SignedContractService.get_all_open_signed_contracts()
        for sc_to_check in signed_contracts_to_check:
            print('signed_c to check: ' + sc_to_check._hash)
            end_time = sc_to_check.signed_timestamp + sc_to_check.duration
            now = int(time.time())
            print('end time=' + str(end_time) + '  now=' + str(now) + '   end<=now= ' + str(end_time<=now))
            if end_time <= now:
                rs = RedisService()
                r = rs._connect()
                prices = r.zrangebyscore('price_stamps', end_time - 2000, end_time + 2000, withscores=True)
                if len(prices) != 0:
                    price = min(prices, key=lambda x: abs(x[1] - end_time))
                    print('terminated contract: ' + sc_to_check._hash)
                    tc = TerminatedContract(sc_to_check._hash, price[0], end_time)
                    terminated_contracts_to_add.append(tc)
                else:
                    print('no prices found')

        last_block_hash = last_block._hash
        miner_pub_key = EcdsaHashing.recover_public_key_str(miner_priv_key)
        height = last_block.height + 1
        block = Block('', '', miner_pub_key, last_block_hash, height, transactions_to_add, pos_transactions_to_add, contract_transactions_to_add, contracts_to_add, signed_contracts_to_add, terminated_contracts_to_add, time.time())
        block.update_signature(miner_priv_key)
        block.update_hash()
        return block

    @staticmethod
    def validate_transaction(balances, transaction):
        # enough funds
        balance = balances.get(transaction.from_addr, 0)
        if balance >= transaction.amount:
            balances[transaction.from_addr] = balances.get(transaction.from_addr) - transaction.amount
            balances[transaction.to_addr] = balances.get(transaction.to_addr, 0) + transaction.amount
            print('Valid Transaction: ' + transaction._hash)
            return True, balances
        else:
            print('Invalid Transaction: ' + transaction._hash)
            return False, balances

    @staticmethod
    def validate_pos_transaction(balances, pos_transaction):
        # enough funds
        balance = balances.get(pos_transaction.from_addr, 0)
        if balance >= pos_transaction.amount:
            balances[pos_transaction.from_addr] = balances.get(pos_transaction.from_addr) - pos_transaction.amount
            print('Valid POS Transaction: ' + pos_transaction._hash)
            return True, balances
        else:
            print('Invalid POS Transaction: ' + pos_transaction._hash)
            return False, balances

    @staticmethod
    def validate_contract_transaction(balances, contract_transaction):
        # enough funds
        sc_balance = balances.get(contract_transaction.signed_contract_addr, (0, 0))
        if contract_transaction.to_symbol == 'TPS':
            if sc_balance[1] >= contract_transaction.amount:
                # TODO doesn't account for profit made but don't know how to check for that here
                balances[contract_transaction.signed_contract_addr] = (sc_balance[0], sc_balance[1] - contract_transaction.amount)
                print('Valid Contract Transaction: ' + contract_transaction._hash)
                return True, balances
        elif contract_transaction.from_symbol == 'TPS':
            if sc_balance[0] >= contract_transaction.amount:
                balances[contract_transaction.signed_contract_addr] = (sc_balance[0] - contract_transaction.amount, sc_balance[1])
                print('Valid Contract Transaction: ' + contract_transaction._hash)
                return True, balances

        print('Invalid Contract Transaction: ' + contract_transaction._hash)
        return False, balances

    @staticmethod
    def validate_contract(balances, contract):
        if contract.rate >= 0 and contract.rate <= 1:
            if contract.created_timestamp < contract.sign_end_timestamp:
                print('Valid Contract: ' + contract._hash)
                return True, balances
        print('Invalid Contract: ' + contract._hash)
        return False, balances

    @staticmethod
    def validate_signed_contract(balances, signed_contract):
        contract = ContractService.get_contract_by_hash(signed_contract.parent_hash)
        if contract != None:
            if signed_contract.amount == contract.amount:
                if signed_contract.signed_timestamp <= contract.sign_end_timestamp:
                    if balances.get(signed_contract.from_addr, 0) >= signed_contract.amount:
                        balances[signed_contract.from_addr] = balances[signed_contract.from_addr] - signed_contract.amount
                        sc_balance = balances.get(signed_contract._hash, (0,0))
                        balances[signed_contract._hash] = (sc_balance[0] + signed_contract.amount, sc_balance[1])
                        print('Valid Signed Contract: ' + signed_contract._hash)
                        return True, balances
                    else:
                        print('insufficient funds')
                else:
                    print('contract timed out')
            else:
                print("amounts don't match")
        else:
            print('contract not found')
        print('Invalid Signed Contract: ' + signed_contract._hash)
        return False, balances

    @staticmethod
    def validate_incoming_block(block):
        block_dal = BlockServiceDal()
        objects = block_dal.get_all_objects_up_to_block(block)
        balances = BlockService.get_all_balances(objects)
        for key in balances.keys():
            balance = balances[key]
            if key != '':
                if type(balance) is tuple:
                    if balance[0] <= 0 or balance[1] <= 0:
                        return False
                else:
                    if balance <= 0:
                        print('insufficient funds on ')
                        return False
        return True