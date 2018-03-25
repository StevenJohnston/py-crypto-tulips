from crypto_tulips.services.block_service import BlockService
from crypto_tulips.services.base_object_service import BaseObjectService

from crypto_tulips.dal.services.signed_contract_service import SignedContractService
from crypto_tulips.dal.services.contract_service import ContractService

from crypto_tulips.dal.objects.block import Block

from crypto_tulips.dal.objects.transaction import Transaction
from crypto_tulips.dal.objects.pos_transaction import PosTransaction
from crypto_tulips.dal.objects.contract_transaction import ContractTransaction
from crypto_tulips.dal.objects.contract import Contract
from crypto_tulips.dal.objects.signed_contract import SignedContract


def create_block():
    balances = BlockService.get_all_balances()

    transactions = BaseObjectService.get_all_mempool_objects(Transaction)
    transactions_to_add = []
    for transaction in transactions:
        if len(transactions_to_add) == 10:
            break
        valid, balances = validate_transaction(balances, transaction)
        if valid:
            transactions_to_add.append(transaction)

    pos_transactions = BaseObjectService.get_all_mempool_objects(PosTransaction)
    pos_transactions_to_add = []
    for pos_transaction in pos_transactions:
        if len(pos_transactions_to_add) == 10:
            break
        valid, balances = validate_pos_transaction(balances, pos_transaction)
        if valid:
            pos_transactions_to_add.append(pos_transaction)

    contract_transactions = BaseObjectService.get_all_mempool_objects(ContractTransaction)
    contract_transactions_to_add = []
    for contract_transaction in contract_transactions:
        if len(contract_transactions_to_add) == 10:
            break
        valid, balances = validate_contract_transaction(balances, contract_transaction)
        if valid:
            contract_transactions_to_add.append(contract_transaction)

    contracts = BaseObjectService.get_all_mempool_objects(Contract)
    contracts_to_add = []
    for contract in contracts:
        if len(contracts_to_add) == 10:
            break
        valid, balances = validate_contract(balances, contract)
        if valid:
            contracts_to_add.append(contract)

    signed_contracts = BaseObjectService.get_all_mempool_objects(SignedContract)
    signed_contracts_to_add = []
    for signed_contract in signed_contracts:
        if len(signed_contracts_to_add) == 10:
            break
        valid, balances = validate_signed_contract(balances, signed_contract)
        if valid:
            signed_contracts_to_add.append(signed_contract)

    block = Block('', '', 'OWNER', 'prev_block', height, transactions_to_add, pos_transactions_to_add, contract_transactions_to_add, contracts_to_add, signed_contracts_to_add, terminated_contracts, time.time())




def validate_transaction(balances, transaction, adding):
    # enough funds
    balance = balances.get(transaction.from_addr, 0)
    if balance >= transaction.amount:
        balances[transaction.from_addr] = balances.get(transaction.from_addr) - transaction.amount
        balances[transaction.to_addr] += balances.get(transaction.to_addr) + transaction.amount
        print('Valid Transaction: ' + transaction._hash)
        return True, balances
    else:
        print('Invalid Transaction: ' + transaction._hash)
        return False, balances

def validate_pos_transaction(balances, pos_transaction, adding):
    # enough funds
    balance = balances.get(pos_transaction.from_addr, 0)
    if balance >= pos_transaction.amount:
        balances[pos_transaction.from_addr] = balances.get(pos_transaction.from_addr) - pos_transaction.amount
        print('Valid POS Transaction: ' + pos_transaction._hash)
        return True, balances
    else:
        print('Invalid POS Transaction: ' + pos_transaction._hash)
        return False, balances

def validate_contract_transaction(balances, contract_transaction, adding):
    # enough funds
    sc_balance = balances.get(contract_transaction.signed_contract_addr, (0, 0))
    if contract_transaction.to_symbol = 'TPS':
        if sc_balance[1] >= contract_transaction.amount:
            # TODO doesn't account for profit made but don't know how to check for that here
            balances[contract_transaction.signed_contract_addr] = (sc_balance[0], sc_balance[1] - contract_transaction.amount)
            print('Valid Contract Transaction: ' + contract_transaction._hash)
            return True, balances
    elif contract_transaction.from_symbol = 'TPS':
        if sc_balance[0] >= contract_transaction.amount:
            balances[contract_transaction.signed_contract_addr] = (sc_balance[0] - contract_transaction.amount, sc_balance[1])
            print('Valid Contract Transaction: ' + contract_transaction._hash)
            return True, balances

    print('Invalid Contract Transaction: ' + contract_transaction._hash)
    return False, balances

def validate_contract(balances, contract, adding):
    if contract.rate >= 0 and contract.rate <= 1:
        if contract.created_timestamp < contract.sign_end_timestamp:
            print('Valid Contract: ' + contract._hash)
            return True, balances
    print('Invalid Contract: ' + contract._hash)
    return False, balances

def validate_signed_contract(balances, signed_contract, adding):
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
    print('Invalid Signed Contract: ' + signed_contract._hash)
    return False