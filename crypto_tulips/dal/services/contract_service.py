import json
import redis
from crypto_tulips.dal.objects.contract import Contract
from crypto_tulips.dal.services.redis_service import RedisService
from crypto_tulips.services.transaction_service import TransactionService
from crypto_tulips.services.contract_transaction_service import ContractTransactionService

from enum import Enum

class ContractFilter:
    CONTRACT_RATE = 'contracts:rate'
    CONTRACT_AMOUNT = 'contracts:amount'
    CONTRACT_START = 'contracts:start'
    CONTRACT_DURATION = 'contracts:duration'
    CONTRACT_END = 'contracts:end'

    def __init__(self, key, minimum, maximum):
        self.key = key
        self.minimum = minimum
        self.maximum = maximum

class ContractService:

    @staticmethod
    def store_contract(contract, pipe = None):
        """
        Store a contract in the database.

        Arguments:
        contract    -- contract object to be store in the database

        Returns:
        list        -- list containing results of each query used to store an object (0s and 1s)
                    0s indicate that the field was updated (already present)
                    1s indicate that the field is new and was stored
            OR
        pipeline    -- pipeline object to continue inserting into redis with (if pipe was passed in)
        """
        rs = RedisService()
        rs.store_object(contract)
        r = rs._connect()
        pipe_created = False
        if pipe == None:
            pipe = r.pipeline()
            pipe_created = True
        pipe.zadd(ContractFilter.CONTRACT_RATE, contract.rate, contract._hash)
        pipe.zadd(ContractFilter.CONTRACT_AMOUNT, contract.amount, contract._hash)
        pipe.zadd(ContractFilter.CONTRACT_START, contract.timestamp, contract._hash)
        pipe.zadd(ContractFilter.CONTRACT_DURATION, contract.duration, contract._hash)
        pipe.zadd(ContractFilter.CONTRACT_END, contract.end_timestamp, contract._hash)

        if pipe_created:
            return pipe.execute()
        else:
            return pipe

    @staticmethod
    def get_contract_by_hash(contract_hash):
        """
        Get a contract by it's hash.

        Arguments:
        contract_hash   -- string of contract's hash to retrieve

        Returns:
        contract    -- contract object
        """
        rs = RedisService()
        return rs.get_object_by_hash(contract_hash, Contract)

    @staticmethod
    def get_contracts_by_range(contract_filters):
        """
        Get contracts for a key between a range.

        Arguments:
        contract_filters    -- list of ContractFilter objects to filter database on

        Returns:
        list    -- list of contracts based on filters passed in
        """
        rs = RedisService()
        r = rs._connect()
        contract_hashes = list()
        for contract_filter in contract_filters:
            hashes = r.zrangebyscore(contract_filter.key, contract_filter.minimum, contract_filter.maximum)
            contract_hashes.extend(hashes)

        contracts = list()
        for contract_hash in contract_hashes:
            contract = rs.get_object_by_hash(contract_hash, Contract, r)
            contracts.append(contract)
        return contracts

    @staticmethod
    def get_investee_for_contract(contract):
        """
        Get the first transaction to a given contract.

        Arguments:
        contract    -- contract object to get investee for
        """
        transactions = TransactionService.get_transactions_to_public_key(contract.addr)
        transactions.sort(key=lambda t: t.timestamp)
        investee_transaction = None
        for transaction in transactions:
            if transaction.amount >= contract.amount:
                investee_transaction = transaction
                break
        return investee_transaction

    @staticmethod
    def get_all_contracts_by_owner(owner_key):
        """
        Get all contracts for a given owner public key.

        Arguments:
        owner_key   -- public key to search database by

        Returns:
        list    -- list of contracts that are owned by the public key supplied
        """

        rs = RedisService()
        r = rs._connect()
        contract_hashes = r.smembers('contract:owner:' + owner_key)
        contracts = list()
        for contract_hash in contract_hashes:
            contract = ContractService.get_contract_by_hash(contract_hash)
            contracts.append(contract)
        return contracts

    @staticmethod
    def get_contract_balance_by_contract_address(contract_addr):
        """
        TODO
        Get balance for a given contract

        Argument:
        contract_addr   -- public key for a given contract

        Returns:
        float   -- current balance on the contract
        """

        rs = RedisService()
        r = rs._connect()
        contract_hashes = r.smembers('contract:addr:' + contract_addr)
        transactions, to_balance = TransactionService.get_transactions_by_public_key(contract.addr)
        contract_transactions, ongoing_balance = ContractTransactionService.get_objects_by_public_key(contract.addr)

        remaining_balance = to_balance + ongoing_balance
        return remaining_balance