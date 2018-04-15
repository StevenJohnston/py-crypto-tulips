import json
import redis
from crypto_tulips.dal.objects.contract import Contract
from crypto_tulips.dal.services.redis_service import RedisService
from crypto_tulips.services.transaction_service import TransactionService
from crypto_tulips.services.contract_transaction_service import ContractTransactionService

class ContractFilter:
    RATE = 'contracts:rate'
    AMOUNT = 'contracts:amount'
    CREATED = 'contracts:created'
    DURATION = 'contracts:duration'
    SIGN_END = 'contracts:sign_end'

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
        pipe.zadd(ContractFilter.RATE, contract.rate, contract._hash)
        pipe.zadd(ContractFilter.AMOUNT, contract.amount, contract._hash)
        pipe.zadd(ContractFilter.CREATED, contract.created_timestamp, contract._hash)
        pipe.zadd(ContractFilter.DURATION, contract.duration, contract._hash)
        pipe.zadd(ContractFilter.SIGN_END, contract.sign_end_timestamp, contract._hash)

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

        if not contract_filters:
            if include_mempool:
                in_mempool_list = r.smembers('contract:is_mempool:1')
                in_mempool_set = set()
                for mem_hash in in_mempool_list:
                    in_mempool_set.add(mem_hash[9:]) # remove 'contract:' from the beginning of the key
                contract_hashes = in_mempool_set.union(mempool_set)
            else:
                contract_hashes = mempool_set.copy()
        else:
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
            print(contract_hash)
            contract = rs.get_object_by_hash(contract_hash, Contract, r)
            contracts.append(contract)
        contracts.sort(key=lambda c: (-c.created_timestamp))
        return contracts[:50]

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