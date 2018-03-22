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
    CONTRACT_CREATED = 'contracts:created'
    CONTRACT_DURATION = 'contracts:duration'

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
        pipe.zadd(ContractFilter.CONTRACT_CREATED, contract.timestamp, contract._hash)
        pipe.zadd(ContractFilter.CONTRACT_DURATION, contract.duration, contract._hash)

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
    def get_contract_by_full_key(contract_key):
        """
        Get a contract by it's full key.

        Arguments:
        contract_key    -- string on contract's key to retrieve

        Returns:
        contract    -- contract object
        """
        rs = RedisService()
        return rs.get_object_by_full_key(contract_key, Contract)

    @staticmethod
    def get_contracts_by_filter(contract_filters, include_mempool):
        """
        Get contracts by a filter.

        Arguments:
        contract_filters    -- list of ContractFilter objects to filter database on
        include_mempool     -- True if results should include those in the mempool, false otherwise

        Returns:
        list    -- list of contracts based on filters passed in
        """
        rs = RedisService()
        r = rs._connect()

        contract_hashes = set()
        temp_hashes = set()
        mempool_list = list()
        mempool_set = set()
        if not include_mempool:
            mempool_list = r.smembers('contract:is_mempool:0')
            for mem_hash in mempool_list:
                mempool_set.add(mem_hash[9:]) # remove 'contract:' from the beginning of the key

        for contract_filter in contract_filters:
            print("key: " + contract_filter.key + " | range: " + str(contract_filter.minimum) + "->" + str(contract_filter.maximum))
            hashes = r.zrangebyscore(contract_filter.key, contract_filter.minimum, contract_filter.maximum)
            temp_hashes = set(hashes)
            # if first filter
            if len(contract_hashes) == 0:
                contract_hashes = temp_hashes.copy()
                # if mempool contracts are to be ignored
                if not include_mempool:
                    contract_hashes = contract_hashes.intersection(mempool_set)
                temp_hashes.clear()
            else:
                # after first filter
                contract_hashes = contract_hashes.intersection(temp_hashes)

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
        transactions = TransactionService.get_transactions_to_public_key(contract.addr, False)
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
            contract = ContractService.get_contract_by_full_key(contract_hash)
            contracts.append(contract)
        return contracts

    @staticmethod
    def get_contract_balance_by_contract_address(contract_addr):
        """
        Get balance for a given contract

        Argument:
        contract_addr   -- public key for a given contract

        Returns:
        float   -- current balance on the contract
        """

        rs = RedisService()
        r = rs._connect()
        contract_hashes = r.smembers('contract:addr:' + contract_addr)
        transactions, starting_balance = TransactionService.get_transactions_by_public_key(contract.addr)
        contract_transactions = ContractTransactionService.get_contract_transactions_for_contract_address(contract.addr, False)

        # have starting balance
        for ct in contract_transactions:
            if ct.to_symbol == 'TPS':

        return remaining_balance

    @staticmethod
    def get_contract_start_time(contract):
        t = ContractService.get_investee_for_contract(contract)
        return t.timestamp